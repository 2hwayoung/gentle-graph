import sys
sys.path.append("/home/capje/kafka_tool/")

import time
import unicodedata as unicode
# from kafka_module import Producer
# from kafka_module import Consumer
from pororo import Pororo
import os
import json
from tqdm import tqdm
STOPWORDS = ["한국일보", "매일경제", "일다", "이코노미스트", "조선일보", "국민일보", "MBN", "시사IN", "이데일리", "한경비즈니스", "서울신문", "월간 산", "더팩트", "헤럴드경제", "한국경제", "블로터", "SBS Biz", "뉴스1", "헬스조선", "디지털데일리", "YTN", "중앙SUNDAY", "코메디닷컴", "디지털타임스", "한겨레21", "노컷뉴스", "JTBC", "파이낸셜뉴스", "서울경제", "중앙일보", "세계일보", "매일신문", "TV조선", "동아일보", "기자협회보", "오마이뉴스", "한겨레", "매경이코노미", "경향신문", "한국경제TV", "여성신문", "강원일보", "코리아중앙데일리", "연합뉴스", "연합뉴스TV", "문화일보", "시사저널", "비즈니스워치", "신동아", "조세일보", "머니투데이", "레이디경향", "주간경향", "미디어오늘", "채널A", "부산일보", "프레시안", "동아사이언스", "코리아헤럴드", "ZDNet Korea", "SBS", "아이뉴스24", "뉴시스", "뉴스타파", "머니S", "데일리안", "전자신문", "조선비즈", "아시아경제", "MBC", "KBS", "주간조선", "주간동아", "JTBC", "아들", "가족", "엄마", "친구", "부모", "한국인", "아빠", "딸", "누나", "오빠", "형", "지인", "아내", "남편", "자녀", "자식"]


# producer = Producer("/home/capje/kafka_tool/config.yaml", value_type="json")
# consumer = Consumer("/home/capje/kafka_tool/config.yaml", 'preprocessor', value_type="json")

def pororo_contents_batch(platform, keys):
    ner = Pororo(task="ner", lang="ko")
    pos = Pororo(task="pos", lang="ko")

    path = '/home/capje/crawling/data/'
    file_list = os.listdir(path)
    file_list_py = [file for file in file_list if file.startswith(platform) and '25' not in file and '26' not in file]
    for i in file_list_py:
        print(path+i)
        with open((path+i), 'r') as f:
            data = json.load(f)

        for d in data:
            keywords = []
            for key in keys:

                if key in ("hashtags", "description"):
                    d[key] = ". ".join(d[key])

                try:
                    ner_result = ner(d[key])
                    # ner_result = [
                    #     v for v, c in ner_result if c not in ["O", "QUANTITY", "DATE"]
                    # ]
                    # keywords += ner_result

                    tmp = set()
                    flag = True

                    for word, tp in ner_result:
                        if tp not in ['DATE', 'QUANTITY', 'O', 'COUNTRY', 'LOCATION', 'OCCUPATION', 'TIME', 'CITY', 'TERM', 'ANIMAL'] and len(word) > 1:
                            if word.isalnum() and (word not in STOPWORDS):
                                for c in word:
                                    if 'HANGUL' not in unicode.name(c) and 'LATIN' not in unicode.name(c) and 'DIGIT' not in unicode.name(c):
                                        flag = False
                                        break
                                
                                if flag:
                                    word = word.upper()
                                    tmp.add(word)
                                    flag = True
                    
                    for word, pos_word in [(word, pos(word)) for word in list(tmp)]:
                        if len(word) == 0 and pos_word != 'NNP':
                            tmp.remove(word)

                    keywords += list(tmp)

                except:
                    continue
                
            d["keyword"] = list(set(keywords))

        out_dir = '/home/capje/crawling/pre_data/pre_'+i
        print(out_dir)
        with open(out_dir, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":

    option = sys.argv[1]

    start = time.perf_counter()
    if option == "naver_news":
        pororo_contents_batch('naver_data', ["title"])
    elif option == "daum_news":
        pororo_contents_batch('daum_data', ["title"])
    elif option == "youtube_contents":
        pororo_contents_batch('youtube_data',
            ["title", "description", "hashtags"],
        )
    end = time.perf_counter()
    print("preprocessing time elapsed: ", end - start)
