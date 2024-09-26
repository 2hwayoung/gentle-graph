import sys
sys.path.append("/home/capje/kafka_tool/")

import os
import re
import time
import datetime
from selenium import webdriver
from fake_useragent import UserAgent
from kafka_module import *

def crawling(chrome_driver_path: str, crawl_time: str):
    # init chrome driver
    chrome_driver = chrome_driver_path

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("headless")
    chrome_options.add_argument("--window-size=1100,2000")
    userAgent = UserAgent().random
    chrome_options.add_argument(f"user-agent={userAgent}")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    prefs = {
        "profile.default_content_setting_values": {
            "cookies": 2,
            "images": 2,
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "auto_select_certificate": 2,
            "fullscreen": 2,
            "mouselock": 2,
            "mixed_script": 2,
            "media_stream": 2,
            "media_stream_mic": 2,
            "media_stream_camera": 2,
            "protocol_handlers": 2,
            "ppapi_broker": 2,
            "automatic_downloads": 2,
            "midi_sysex": 2,
            "push_messaging": 2,
            "ssl_cert_decisions": 2,
            "metro_switch_to_desktop": 2,
            "protected_media_identifier": 2,
            "app_banner": 2,
            "site_engagement": 2,
            "durable_storage": 2,
        }
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)

    # go to google trends
    driver.get("https://trends.google.co.kr/trends/trendingsearches/daily?geo=KR")
    trends = driver.find_elements_by_css_selector("div.feed-list-wrapper")
    today_trends = trends[0].find_elements_by_css_selector("feed-item")

    # producer = Producer("/home/capje/kafka_tool/config.yaml")

    trends_list = []
    for trend in today_trends:
        header = trend.find_element_by_css_selector("div.feed-item-header")

        rank = header.find_element_by_css_selector("div.index").text

        keyword = (
            header.find_element_by_css_selector("div.title")
            .find_element_by_css_selector("a")
            .text
        )

        news_url = header.find_element_by_css_selector(
            "div.summary-text > a"
        ).get_attribute("href")

        now = datetime.datetime.now()
        created_time = (
            header.find_element_by_css_selector("div.source-and-time")
            .find_elements_by_css_selector("span")[1]
            .text
        )
        if "시간" in created_time:
            created_time = int(re.findall("\d+", created_time)[0])
            created_time = now - datetime.timedelta(hours=created_time)
        elif "일" in created_time:
            created_time = int(re.findall("\d+", created_time)[0])
            created_time = now - datetime.timedelta(days=created_time)
        else:
            created_time = now

        search_count = header.find_element_by_css_selector(
            "div.search-count-title"
        ).text

        data = {
            "rank": rank,
            "keyword": keyword,
            "news_url": news_url,
            "date": created_time.strftime("%Y-%m-%d"),
            "search_count": search_count,
            "crawl_time": crawl_time
        }

        # producer.send_to_topic(topic="google_trend", value=data)

        trends_list.append(data)

    return trends_list


if __name__ == "__main__":
    crawl_time = time.strftime('%Y-%m-%d/%H', time.localtime(time.time()))
    chrome_driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
    total_data = crawling(chrome_driver_path, crawl_time)

    import json
    with open('./google_data.json','w') as f:
        json.dump(total_data, f, indent="\t", ensure_ascii=False)