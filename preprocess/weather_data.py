####################################날씨 데이터 추가를 위한 셀###############################################
#1) date.txt부터 period, start_month, start_day, end_month, end_day를 가져온다.
#2) period == 0 (행사가 다른 월을 걸쳐 진행된다.)
    # 2)-1 시작월을 크롤링한다.
    # 2)-2시작일부터 해당 월의 마지막까지 가져온다.
    # 2)-3 종료 월을 크롤링한다.
    # 2)-4 종료 일 전까의 데이터를 가져온다. 
#3) period != 0 (행사가 같은 월에 진행된다.)
    # 3)-1 행사 월을 크롤링한다. (start_month)
    # 3)-2 행사 일수를 가져온다. (period)
    # 3)-3 시작일부터 행사 일 수까지 데이터를 크롤링한다. 

import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from openpyxl import load_workbook
from collections import Counter
import os

def crawling_weather(location_code, year, month):
    #혹여나 이전에 에 있던 파일 지우기
    os.remove("weather.txt")
    url = "https://www.weather.go.kr/weather/climate/past_cal.jsp?stn={}&yy={}&mm={}&obs=1&x=18&y=6".format(location_code, year, month)

    #크롬드라이버 설치 위치를 입력해준다. 
    driver = wd.Chrome("C:\/chromedriver")
    driver.get(url)
    time.sleep(2)  #페이지가 완전히 로드될 때까지 기다린다.
    
    #2)-1 시작월의 날씨 정보를 크롤링한다. 
    data = []
    table = driver.find_element_by_css_selector('table.table_develop')
    contents = table.find_element_by_tag_name('tbody')
    contents = contents.text
    
    # 날씨 정보를 weather.txt에 저장한다. 
    contents = contents.strip()
    weather_file = open("weather.txt", 'w')
    weather_file.write(contents)
    weather_file.close()
    driver.close()

def start_weather(infos, start_day):
    f= open("weather.txt", 'r')
    s= f.readlines()
    days = []
    lis = []
    index = 100
    info_count = 0 
    for_dic = []
    count = -1

    ## 시작일 이후부터 저장
    for i in s:
        i = i.strip('\n')
        days = i.split(" ")
        if ((str(start_day) + "일") in days):
            i = i.strip('\n')
            days = i.split(" ")
            #위치 찾기
            index = days.index(str(start_day) + "일") 
            print(index)
            count = -1

        if (index != 100):
            count += 1

        if(count > index*5):
            i = i.replace('\n', " ")            
            if("일 " not in i):
                for_dic = []
                data = i.strip('\n')
                data = data.strip()
                data = data.split(":")
                for_dic.append(data)
                for_dic = dict(for_dic)
                lis.append(for_dic)
                info_count += 1
                if(info_count == 5):
                    infos.append(lis)
                    info_count = 0
                    lis = []
    f.close()

def end_weather(infos, end_day):
    f= open("weather.txt", 'r')
    s= f.readlines()
    days = [] #일들을 담는 리스트
    lis = [] #행사 하나를 의미하는 리스트
    for_dic = [] # 딕셔너리로 만들기 위한 리스트
    index = 100 
    count = -1
    info_count = 0 
    #조건문에서 infos 길이와 end day를 비교하는데, start_day 만큼 더해져있기에 나중에 빼주기 위함
    infos_len = len(infos)

    ## 만약에 종료일이 3일이다
    for i in s:
        i = i.rstrip('\n')
        days = i.split(" ")
        if ((str(end_day)+"일") in days):
            i = i.rstrip('\n')
            days = i.split(" ")
            #위치 찾기
            index = days.index(end_day+"일") 
            break
            
    info_count = 0
    for again in s:
        if(len(infos)-infos_len == int(end_day)):
            break
        else:
            again = again.replace('\n', " ")
            if("일 " not in again):
                for_dic = []
                again = again.rstrip('\n')
                again = again.strip()
                again = again.split(':')
                for_dic.append(again)
                for_dic = dict(for_dic)
                lis.append(for_dic)
                info_count += 1
                if(info_count == 5):
                    infos.append(lis)
                    info_count = 0
                    lis = []
    f.close()


def same_weather(infos, period, start_day):
    f= open("weather.txt", 'r')
    s= f.readlines()
    days = [] #일들을 담는 리스트
    lis = [] #행사 하나를 의미하는 리스트
    for_dic = [] # 딕셔너리로 만들기 위한 리스트
    index = 100 
    count = -1
    info_count = 0 

   ## 시작일 이후부터 저장
    for i in s:
        if(len(infos) == int(period)):
            break

        i = i.strip('\n')
        days = i.split(" ")
        

        if ((str(start_day) + "일") in days):
            #위치 찾기
            index = days.index(str(start_day) + "일") 
            count = -1

        if (index != 100):
            count += 1

        if(count > index*5):
            i = i.replace('\n', " ")
            if("일 " not in i):
                for_dic = []
                data = i.strip('\n')
                data = data.strip()
                data = data.split(":")
                for_dic.append(data)
                for_dic = dict(for_dic)
                lis.append(for_dic)
                info_count += 1
                if(info_count == 5):
                    infos.append(lis)
                    info_count = 0
                    lis = []
                    
        f.close()

def calc(infos):
    weather_info = []
    sum_avg_temp = 0.0 
    sum_high_temp = 0.0 
    sum_low_temp = 0.0
    sum_avg_cloud = 0.0  
    sum_rain = 0.0 
    weather = ""
    for day in infos:
        try:
            sum_avg_temp += float((day[0].get('평균기온')).replace("℃", ""))
            sum_high_temp += float((day[1].get('최고기온')).replace("℃", ""))
            sum_low_temp += float((day[2].get('최저기온')).replace("℃", ""))
            if((day[3].get('평균운량')) == ' -'):
                sum_avg_cloud += 0
            else:      
                sum_avg_cloud += float((day[3].get('평균운량')))

            if((day[4].get('일강수량')).replace("mm", "") == ' -'):
                sum_rain += 0
            else:
                sum_rain += float((day[4].get('일강수량')).replace("mm", ""))
        except:
            weather = "None\n"
     
    if(weather != "None\n"):       
        #축제별 avg_temp, high_temp, low_temp, avg_cloud, rain
        count = len(infos)
        avg_temp = round(sum_avg_temp/count, 2)
        high_temp = round(sum_high_temp/count)
        low_temp = round(sum_low_temp/count, 2)
        avg_cloud = round(sum_avg_cloud/count)
        rain = round(sum_rain/count, 2)   
        weather =  str(avg_temp) + ", " + str(high_temp) + ", " + str(low_temp) + ", " + str(avg_cloud) + ", " +str(rain)+ "\n"
    
    f = open("weather_info.txt", 'a')
    f.write(weather)
    f.close()



###############시작####################
#1) date.txt부터 period, start_month, start_day, end_month, end_day를 가져온다.
f = open("date.txt", 'r')
lines = f.readlines()
for line in lines:
    infos = []
    line = line.strip("\n")
    date = line.split(",")

    year = 2017
    period = date[0]
    start_month = date[1]
    start_day = date[2]
    end_month = date[3]
    end_day = date[4]
    location_code = date[5]
    if(location_code == "163"):
        location_code = 165
    print (year,"년 ", start_month, "월 ", start_day, "일 ~ ", year, "년 ", end_month, "월 ", end_day, "일")
    print("기간: ", period)


    #2) period == 0 (행사가 다른 월을 걸쳐 진행된다.)
    if period == '0':
        # 2)-1 시작월을 크롤링한다. (start_month)
        print("start crawling")
        crawling_weather(location_code, year, start_month)
        # 2)-2시작일부터 해당 월의 마지막까지 가져온다.
        start_weather(infos, start_day)
        print("start_infos: ", infos)
        # 2)-3 종료 월을 크롤링한다.
        crawling_weather(location_code, year, end_month)
        # 2)-4 종료 일 전까의 데이터를 가져온다.
        end_weather(infos, end_day)
        print("end_infos: ", infos)
        # 2)-5 각각의 날씨를 계산한다.
        calc(infos)


    else:
        print("same month")
        # 3)-1 행사 월을 크롤링한다. (start_month)
        crawling_weather(location_code, year, start_month)
        # 3)-3 시작일부터 행사 일 수까지 데이터를 크롤링한다. 
        same_weather(infos, period, start_day)
        print("same_infos: ", infos)
        # 3)-4 각각의 날씨를 계산한다.
        calc(infos)
        

f.close()
