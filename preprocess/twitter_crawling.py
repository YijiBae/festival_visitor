fesitival = ['보령머드축제', '고령대가야체험축제', '연천전곡리구석기축제', '진주남강유등축제', '춘천국제마임축제', '강진청자축제', '정선아리랑제', '인천펜타포트축제', '봉화은어축제', '성웅 이순신 축제', '서산해미읍성축제', '고창 모양성제', '영덕대게축제', '울산옹기축제', '통영한산대첩축제', '정남진장흥물축제', '지리산한방약초축제', '창원가고파국화축제', None, '축제명', '펜타포트락페스티벌', '부여서동연꽃축제', '이천쌀문화축제', '금산인삼축제', '강릉커피축제', '담양 대나무 축제', '하동야생차문화축제', '밀양아리랑대축제', '청결고추축제', '산청한방약초축제', '강경전통맛갈젓축제', '완주와일드푸드축제', '남도음식문화큰잔치', '평창효석문화제', '제주왕벚꽃축제', '문경찻사발축제', '제주정월대보름축제', '진도신비의바닷길축제', '전곡리구석기축제', '안동국제탈춤페스티발', '대구약령시한방문화축제', '풍기인삼축제', '광주7080충장축제', '외고산 옹기축제', '함평나비축제', '천안흥타령축제', '동래읍성역사축제', '순창장류축제', '대전효문화뿌리축제', '포항불빛축제', '최남단방어축제', '다향제', '전국음성품바축제', '난계국악축제', '목포해양문화축제', '금강여울축제', '하이서울페스티발', '추억의7080장축제', '제주들불축제', '봉화송이축제', '부산자갈치축제', '영동난계국악축제', '과천한마당축제', '괴산고추축제', '해운대모래축제', '담양대나무축제', '해미읍성역사체험축제', '성북다문화음식축제', '부평풍물대축제', '시흥갯골축제', '함양산삼축제', '무안 백련축제', '원주다이내믹댄싱카니발', '광주추억의충장축제', '무주반딧불축제', '울산고래축제', '광주김치대축제', '경주신라소리', '김해분청도자기축제', '보성다향대축제', '김제지평선축제', '광산우리밀축제', '강원고성명태축제', '원주한지문화제', '여주오곡나루축제', '도두오래물축제', '자라섬재즈페스티벌', '한산모시문화제', '남원춘향제', '경주한국의술과떡축제', '한성백제문화제', '태백산눈꽃축제', '빙어축제', '기지시줄다리기민속축제', '정월대보름축제', '인천소래포구축제', '서귀포칠십리축제', '영암왕인문화축제', '목포항구축제', '충주세계무술축제', '얼음나라화천산천어축제', '대전사이언스페스티발']


import datetime
import GetOldTweets3 as got
import time
from random import uniform
from tqdm import tqdm_notebook
import re
import pandas as pd
import csv
import os

days_range = []
years = ['2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']

twitter_df = pd.DataFrame(columns = ["fesitival", "text", "hashtags", "year"])


for fes in fesitival:
    print("*************여기부터 {}!!!!*************".format(fes)) 
    file_name = str(fes)+".csv"
    for year in years:
        s_date = year + "-01" + "-01"
        e_date = year + "-12" + "-31"

        start = datetime.datetime.strptime(s_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(e_date, "%Y-%m-%d")
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

        for date in date_generated:
            days_range.append(date.strftime("%Y-%m-%d"))

        print("=== 설정된 트윗 수집 기간은 {} 에서 {} 까지 입니다 ===".format(days_range[0], days_range[-1]))
        print("=== 총 {}일 간의 데이터 수집 ===".format(len(days_range)))


        start_date = days_range[0]
        end_date = (datetime.datetime.strptime(days_range[-1], "%Y-%m-%d") 
                    + datetime.timedelta(days=1)).strftime("%Y-%m-%d") 

        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(fes)\
                                                   .setSince(start_date)\
                                                   .setUntil(end_date)\
                                                   .setMaxTweets(-1)

        start_time = time.time()

        tweet = got.manager.TweetManager.getTweets(tweetCriteria)

        print("=== Total num of tweets is {} ===".format(len(tweet)))


        tweet_list = []

        for index in tqdm_notebook(tweet):

            content = index.text
            hashtags = []

            #content 전처리
            #1) 해시태그 분리하다.
            tags = re.findall('#[A-Za-z0-9가-힣]+', content)
            tag = ''.join(tags).replace('#', " ") # "#" w제거
            tag_data = tag.split()
            for tag_one in tag_data:
                hashtags.append(tag_one) 

            #2) pure한 content 만들기
            content = content.replace('#', '')
            content = content.replace(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '')

            # 결과 합치기
            info_list = [fes, content, hashtags, year]
            tweet_list.append(info_list)

            # 휴식 
            time.sleep(uniform(1,2))

        twitter_df = pd.DataFrame(tweet_list, columns = ["fesitival", "text", "hashtags", "year"]).append(twitter_df, ignore_index=True)

    twitter_df.to_csv(file_name.format(days_range[0], days_range[-1]), index=False)
    print("=== new file and {} tweets are successfully saved ===".format(len(tweet_list)))  
    print("*************여기까지가 {} 관련된 것이비다요*************".format(fes))  