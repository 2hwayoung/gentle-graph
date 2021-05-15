import os
import sys
sys.path.append("/home/capje/kafka_tool/")
sys.path.append("/home/capje/neo4j_query/")

from test_ver_2 import naver_neo4j, daum_neo4j, youtube_neo4j
from kafka_module import Consumer
from tqdm import tqdm

from config import CONFIG
from config import TEST_CONFIG


if __name__ == "__main__":
    
    contents_type = sys.argv[1]

    consumer = Consumer("/home/capje/kafka_tool/config.yaml", "neo4j_insert", value_type="json")

    if contents_type == "naver_news":

        app = naver_neo4j.App(CONFIG["bolt_url"], CONFIG["user"], CONFIG["password"])
        platform = 'Naver'

        data = consumer.get_data(topic='naver_news_2')

        json_data = [d.value for d in data]

        print(json_data[:2])
        
        for value in tqdm(json_data):
            app.create_crawltime(value['crawl_time'])
            app.create_creator_and_match_platform(value['press'], platform)

            app.create_content_and_match_with_info(value['url'], value['title'], value['date'], value['n_view'], value['n_comment'], \
                value['n_reaction_good'], value['n_reaction_warm'], value['n_reaction_sad'], \
                value['n_reaction_angry'], value['n_reaction_want'], \
                value['crawl_time'], 'bestview', value['rank'], value['press'], platform)

            for elem in value['keyword']:
                app.create_keyword(elem)
                app.match_content_and_keyword(elem, value['url'], value['title'], value['date'], value['n_view'], value['n_comment'], \
                    value['n_reaction_good'], value['n_reaction_warm'], value['n_reaction_sad'], \
                    value['n_reaction_angry'], value['n_reaction_want'])
                    
        app.close()


    elif contents_type == "daum_news":

        app = youtube_neo4j.App(CONFIG["bolt_url"], CONFIG["user"], CONFIG["password"])
        platform = 'Daum'

        data = consumer.get_data(topic='daum_news_2')

        json_data = [d.value for d in data]
        
        for value in tqdm(json_data):
            app.create_crawltime(value['crawl_time'])
            app.create_creator_and_match_platform(value['press'], platform)

            if value['category'] == 'age':
                app.create_content_and_match_with_info_classified_by_age(value['url'], value['title'], value['date'], value['n_comment'], \
                    value['n_reaction_recommend'], value['n_reaction_like'], value['n_reaction_impress'], \
                    value['n_reaction_angry'], value['n_reaction_sad'], value['crawl_time'], \
                    value['category'], value['age'], value['sex'], value['rank'], value['press'], platform)

            else:
                app.create_content_and_match_with_info(value['url'], value['title'], value['date'], value['n_comment'], \
                    value['n_reaction_recommend'], value['n_reaction_like'], value['n_reaction_impress'], \
                    value['n_reaction_angry'], value['n_reaction_sad'], \
                    value['crawl_time'], value['category'], value['rank'], value['press'], platform)

            for elem in value['keyword']:
                app.create_keyword(elem)
                app.match_content_and_keyword(elem, value['url'], value['title'], value['date'], value['n_comment'], \
                    value['n_reaction_recommend'], value['n_reaction_like'], value['n_reaction_impress'], \
                    value['n_reaction_angry'], value['n_reaction_sad'])
                    
        app.close()


    elif contents_type == "youtube_contents":

        app = daum_neo4j.App(CONFIG["bolt_url"], CONFIG["user"], CONFIG["password"])
        
        platform = 'Youtube'

        data = consumer.get_data(topic='youtube_contents_2')
        
        json_data = [d.value for d in data]

        for value in tqdm(json_data):
            app.create_crawltime(value['crawl_time'])
            app.create_creator_and_match_platform(value['creator'], value['creator_url'], platform)

            app.create_content_and_match_with_info(value['url'], value['title'], value['date'], value['n_views'], value['n_comment'], \
                value['n_reaction_good'], value['n_reaction_bad'], value['hashtags'], value['description'], \
                value['crawl_time'], 'korea_popular', value['rank'], value['creator'], platform)

            for elem in value['keyword']:
                app.create_keyword(elem)
                app.match_content_and_keyword(elem, value['url'], value['title'], value['date'], value['n_views'], value['n_comment'], \
                    value['n_reaction_good'], value['n_reaction_bad'], value['hashtags'], value['description'])
            
        app.close()

    elif contents_type == "naver_news_test":

        app = naver_neo4j.App(TEST_CONFIG["bolt_url"], TEST_CONFIG["user"], TEST_CONFIG["password"])
        
        platform = 'Naver'

        data = consumer.get_data(topic='naver_news_2')
        
        json_data = [d.value for d in data]

        for value in tqdm(json_data):
            app.create_content(value['url'], value['title'], value['date'], value['n_view'], value['n_comment'], \
                value['n_reaction_good'], value['n_reaction_warm'], value['n_reaction_sad'], \
                value['n_reaction_angry'], value['n_reaction_want'], \
                value['crawl_time'], 'bestview', value['rank'], value['press'], platform)

            for elem in value['keyword']:
                app.create_keyword(elem)
                app.match_content_and_keyword(elem, value['url'], value['title'], value['date'], value['n_view'], value['n_comment'], \
                    value['n_reaction_good'], value['n_reaction_warm'], value['n_reaction_sad'], \
                    value['n_reaction_angry'], value['n_reaction_want'])
                
                

