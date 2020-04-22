######################################최종##########################################

#감정분석 작업하기
# 1) 형태소로 나눈다. 
# 2) 불용어를 제거한다.
# 3) 형태소별 극성을 계산한다. 
#    어근 :  r_word
#    극성 :  s_word

import json
from konlpy.tag import Hannanum

# 인스타그램 content을 읽어온다. 
content = "나는 니가 정말 싫어"

#1) 형태소로 나눈다. 
content_morphs = []
hannanum = Hannanum()
content_morphs = hannanum.morphs(content)
print(content_morphs)

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
print(content_morphs)

#3) 형태소별 극성 계산
    # data: 감성사전

with open('data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
    data = json.load(f)

for wordname in content_morphs:
    score = 0
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
            
print("content: ", content)
print("score: ", score)
print("polarity: ", polarity)