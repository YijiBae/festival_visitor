import csv
import json
from konlpy.tag import Hannanum
import pandas as pd

def sentiment_analysis(tweet, tweets):
    #1) 형태소로 나눈다. 
    content = tweet[1]
    content_morphs = []
    hannanum = Hannanum()
    content_morphs = hannanum.morphs(content)
 #   print("형태소 분류: ", content_morphs)

    #1)-2 띄어쓰기로 나눈다. 
    space = content.split(" ")
    print(space)

    #2) 불용어 제거하기
    # 2) -1 불용어 불어오기 stopwords => 불용어 리스트
    stopwords_file=open("불용어.txt", 'r', encoding = 'utf-8')
    stopwords = []
    lines = stopwords_file.readlines()
    for line in lines:
        line = line.replace("\n", "")
        stopwords.append(line)

    # 2) -2 불용어 제거하기 
    for i in content_morphs:
        if i in stopwords:
            content_morphs.remove(i)
#    print("불용어 제거: " ,content_morphs)

    #3) 형태소별 극성 계산
        # data: 감성사전
    with open('data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
        data = json.load(f)
    
    score = 0
    for wordname in space:
        for i in range(0, len(data)):
            #어근 비교 및 단어 비교를 같이 한다.
            if (data[i]['word_root'] == wordname) or (data[i]['word'] == wordname):
                if data[i]['polarity'] != "None":
                    score += int(data[i]['polarity'])
                    break
        if score > 0:
            polarity = "positive"
        elif score == 0:
            polarity = "neutral"
        else:
            polarity = "negative"
 
    tweet[4] = polarity
#    hashtag_sentiment_analysis(tweet, tweets)
    tweets.append(tweet)
    print("content: ", content)
    print("polarity: ", polarity)


def hashtag_sentiment_analysis(tweet, tweets):
    hashtags = tweet[2]
    print(hashtags)
    h_polarity = []
    h_score = []

    for hashtag in hashtags:
        score = 0
        #감성사전
        with open('data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
            data = json.load(f)

        for i in range(0, len(data)):
            #어근 비교 및 단어 비교를 같이 한다
            if (data[i]['word_root'] == hashtag) or (data[i]['word'] == hashtag):
                if data[i]['polarity'] != "None":
                    score += int(data[i]['polarity'])
                    break
        if score > 0:
            polarity = "positive"
        elif score == 0:
            polarity = "neutral"
        else:
            polarity = "negative"
        h_polarity.append(polarity)
        h_score.append(score)    

    tweet[6] = h_polarity
    tweet[7] = h_score          
    tweets.append(tweet)

def add_col(fes):
    data = pd.read_csv("data/"+fes+".csv")
    data["polarity"] = " "
    data["score"] = 0
    data.to_csv("data/"+fes+".csv", index=False)

#파일 열기
tweetFile = open('data/고령대가야체험축제.csv','r', encoding='utf-8')
rdr = csv.reader(tweetFile)
tweets = [] 
for tweet in rdr:
    print()
    if(tweet[1] != 'text'):
        sentiment_analysis(tweet, tweets)
#파일 저장
tweetFile = open('data/고령대가야체험축제.csv','w', newline= '', encoding='utf-8')
wr = csv.writer(tweetFile)
wr.writerows(tweets)
tweetFile.close()

