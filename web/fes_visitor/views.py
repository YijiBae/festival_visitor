from django.shortcuts import render
from fes_visitor.forms import Form
from fes_visitor.forms import Option
import pandas as pd
from pandas import DataFrame as df

import datetime
from openpyxl import load_workbook
from sklearn.linear_model import LinearRegression

def calc_day(start_year, start_month, start_day, end_year, end_month, end_day):
    start_date = datetime.datetime(start_year, start_month, start_day)
    end_date = datetime.datetime(end_year, end_month, end_day)
    day_term = (end_date - start_date).days
    return day_term

def calc_else(fes_name):
    #엑셀파일 불러오기
    count = 0
    lists = load_workbook('C:/Users/samsung/Desktop/2020-1/데이터캡스톤디자인/지역축제 방문객 예측/프로젝트/web/fes_visitor/통합축제데이터.xlsx')
    sheet = lists['Sheet1']
    for i in sheet: 
        count += 1
        #제일 첫 열이 None이라서 넘어가는 것
        if(count > 1):                
            if(i[3].value == fes_name):
                KTX = i[11].value
                neutral = i[21].value
                positive = i[22].value
                평균기온절대값 = i[24].value
                최저기온절대값 = i[25].value
                최고기온절대값 = i[26].value
                평균운량 = i[18].value
                평균방문객 = i[27].value
                break
    return KTX, 평균기온절대값, 최저기온절대값, 최고기온절대값, 평균운량, positive, neutral, 평균방문객

def regression_model(test_value):
    festival_df = pd.read_excel('C:/Users/samsung/Desktop/2020-1/데이터캡스톤디자인/지역축제 방문객 예측/프로젝트/web/fes_visitor/통합축제데이터.xlsx', header = 0, sheet_name = 'Sheet1')
    #있는 것 만으로 감정분석
    sentiment = festival_df.dropna(axis=0)
    x_train = sentiment[['기간', "KTX역",'평균기온 절대값', '최저기온 절대값', '최고기온 절대값','평균운량', 'positive', 'neutral', '평균방문객']]
    y_train = sentiment[['합계']]
    
    mlr= LinearRegression()
    mlr.fit(x_train, y_train)
    y_predict = mlr.predict(test_value)
    return y_predict

def bass_model(fes_name, start_year):
    lists = load_workbook('C:/Users/samsung/Desktop/2020-1/데이터캡스톤디자인/지역축제 방문객 예측/프로젝트/web/fes_visitor/연속누적방문객.xlsx')
    sheet = lists['BASS']
    count = 0
    check = -1
    for i in sheet: 
        count += 1
        #제일 첫 열이 None이라서 넘어가는 것
        if(count > 1):
            if(i[0].value == fes_name):
                #년도 찾기
                if(start_year == 2007):
                    return (i[1].value)
                    check = 1 
                elif(start_year== 2008):
                    return (i[2].value)
                    check = 1 
                elif(start_year == 2009):
                    return (i[3].value)
                    check = 1 
                elif(start_year == 2010):
                    return (i[4].value)
                    check = 1 
                elif(start_year == 2011):
                    return (i[5].value)
                    check = 1 
                elif(start_year== 2012):
                    return (i[6].value)
                    check = 1 
                elif(start_year == 2013):
                    return (i[7].value)
                    check = 1 
                elif(start_year == 2014):
                    return (i[8].value)
                    check = 1 
                elif(start_year == 2015):
                    return (i[9].value)
                    check = 1 
                elif(start_year == 2016):
                    return (i[10].value)
                    check = 1 
                elif(start_year == 2017):
                    return (i[11].value)
                    check = 1 
                break

def hybrid_model(regression_result, bass_result):
    final_result = (0.6*bass_result + 0.4* regression_result)
    return final_result

def select_page(request):
    if request.method == "POST":
        form = Form(request.POST)
        # form의 내용이 유효하다면 DB에 저장한다. 
        if form.is_valid():
            fes_name = request.POST.get('fes_name')
            name = form.cleaned_data['fes_name']
            start_year = form.cleaned_data['fes_start_year']
            start_month = form.cleaned_data['fes_start_month']
            start_day = form.cleaned_data['fes_start_day']
            end_year = form.cleaned_data['fes_end_year']
            end_month = form.cleaned_data['fes_end_month']
            end_day = form.cleaned_data['fes_end_day']

            day_term = calc_day(start_year, start_month, start_day, end_year, end_month, end_day)
            print(day_term)
            KTX, 평균기온절대값, 최저기온절대값, 최고기온절대값, 평균운량, positive, neutral, 평균방문객 = calc_else(fes_name)
            test_value = df( data = {'기간': [day_term], "KTX역": [KTX],  '평균기온 절대값': [평균기온절대값], '최저기온 절대값': [최저기온절대값], '최고기온 절대값': [최고기온절대값],'평균운량': [평균운량], 'positive': [positive], 'neutral': [neutral], '평균방문객': [평균방문객]})
            test_value

            regression_result = regression_model(test_value)
            bass_result = bass_model(fes_name, start_year)
            final_result = hybrid_model(regression_result, bass_result)
            print(final_result)
            form.save()
    else:
        form = Form()
    
    return render(request, 'select_page.html', {'form':form} )

def result_page(request):
    # DB에서 결과값 가져오기
    results = Option.objects.all()
    return render(request, 'result_page.html' , {'results': results})