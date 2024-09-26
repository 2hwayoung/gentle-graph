import sys
sys.path.append("/home/capje/kafka_tool/")

import os
import re
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
from fake_useragent import UserAgent
# from kafka_module import Producer
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def str_to_int(string: str):
    value = 0
    if "만" in string:
        value = float(re.findall("\d+\.*\d*", string)[0])
        value *= 10000
    elif "천" in string:
        value = float(re.findall("\d+\.*\d*", string)[0])
        value *= 1000
    else:
        tmp = re.findall("\d+\.*\d*", string)
        if len(tmp) == 0:
            value = 0
        else:
            value = float(tmp[0])

    return int(value)


def crawl_detail_content(driver, data: dict) -> dict:

    if data == None:
        raise ValueError

    # go to content detail page
    driver.get(data["url"], verify=False)
    js = 'document.getElementsByClassName("ytp-play-button ytp-button")[0].click()'
    driver.execute_script(js)

    try:
        js = 'document.getElementsByClassName("more-button style-scope ytd-video-secondary-info-renderer")[0].click()'
        driver.execute_script(js)
    except:
        pass

    driver.execute_script("window.scrollTo(0, 1500);")
    driver.implicitly_wait(3)

    # get detail information of content
    try:
        views = driver.find_element_by_css_selector(
            "#count > ytd-video-view-count-renderer > span.view-count.style-scope.ytd-video-view-count-renderer"
        ).text.replace(",", "")
        views = int(re.findall("\d+", views)[0])
    except:
        views = 0
    try:
        date = (
            driver.find_element_by_css_selector("#date > yt-formatted-string")
            .text.replace(".", "")
            .split()
        )
        date = f"{date[0]}-{date[1]}-{date[2]}"
    except:
        date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    
    try:
        good = (
            driver.find_element_by_css_selector(
                "#top-level-buttons > ytd-toggle-button-renderer:nth-child(1) > a"
            )
            .find_element_by_css_selector("#text")
            .text
        )
    except:
        good = 0

    try:
        bad = (
            driver.find_element_by_css_selector(
                "#top-level-buttons > ytd-toggle-button-renderer:nth-child(2) > a"
            )
            .find_element_by_css_selector("#text")
            .text
        )
    except:
        bad = 0

    # 댓글 기능이 중지된 게시물도 있음
    try:
        comments = driver.find_element_by_css_selector(
            "#count > yt-formatted-string > span:nth-child(2)"
        ).text
        comments = int(comments.replace(",", ""))
    except:
        comments = -1

    time.sleep(2)

    # get content description and hashtags
    try:
        description = driver.find_element_by_css_selector("#description")
        hashlist = description.find_elements_by_css_selector("a")
        texts = description.find_elements_by_css_selector("span")
        hashtags = [
            tag.text
            for tag in hashlist
            if tag.text not in ("", " ") and tag.text.startswith("#")
        ]
        descriptions = [span.text for span in texts if span.text not in (" ", "")]
    except:
        descriptions = ["",]  

    # append detail data
    data.update(
        {
            "n_views": views,
            "date": date,
            "n_reaction_good": str_to_int(good),
            "n_reaction_bad": str_to_int(bad),
            "n_comment": comments,
            "hashtags": hashtags,
            "description": descriptions,
        }
    )

    # producer.send_to_topic(topic="youtube_contents", value=data)

    return data


def crawling(chrome_driver_path: str, crawl_time : str):
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

    # get playlists
    driver.get(
        "https://www.youtube.com/playlist?list=PLmtapKaZsgZt3g_uAPJbsMWdkVsznn_2R"
    )
    driver.execute_script("window.scrollTo(0, 20000);")
    driver.implicitly_wait(5)
    time.sleep(2)
    playlist = driver.find_elements_by_css_selector(
        "ytd-playlist-video-renderer.style-scope.ytd-playlist-video-list-renderer"
    )

    # get brief info
    total_contents = []
    for content in playlist:
        try:
            index = int(content.find_element_by_css_selector("#index").text)
        except:
            index = 0
        video_info = content.find_element_by_css_selector("a#video-title")
        channel_info = content.find_element_by_css_selector(
            "ytd-channel-name#channel-name"
        ).find_element_by_css_selector("a")
        url = video_info.get_attribute("href")
        title = video_info.text
        creator = channel_info.text
        creator_channel = channel_info.get_attribute("href")

        data = {
            "rank": index,
            "url": url,
            "title": title,
            "creator": creator,
            "creator_url": creator_channel,
            "crawl_time" : crawl_time
        }
        total_contents.append(data)

    # producer = Producer("/home/capje/kafka_tool/config.yaml")

    # get detail info
    for content in tqdm(total_contents):
        crawl_detail_content(driver, content)

    return total_contents


if __name__ == "__main__":
    crawl_time = time.strftime('%Y-%m-%d/%H', time.localtime(time.time()))
    chrome_driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
    total_data = crawling(chrome_driver_path, crawl_time)

    import json
    import datetime
    time_str = datetime.datetime.now().strftime('%Y-%m-%d-%H')
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'data_0515/youtube_data_{time_str}.json') 
    
    with open(out_dir, 'w') as f:
        json.dump(total_data, f, indent="\t", ensure_ascii=False)