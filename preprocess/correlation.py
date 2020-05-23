#정규화 방문객 pandas dataframe 만들기
import numpy as np
import pandas as pd

festival_df = pd.read_excel('통합축제데이터.xlsx', header = 0, sheet_name = 'Sheet1')

#있는 것 만으로 감정분석
sentiment= festival_df[festival_df["positive"] > 0]

# 필요한 값에 따라 정규화된 축제인원과의 상관관계 분석
variance = ['기간', "KTX역",'경제효과', '평균기온','최고기온', '최저기온','평균운량','평균강수량', '평균기온 절대값', '최저기온 절대값', 'positive', 'negative']
for i in variance:
    corr = sentiment[i].corr(sentiment['축제인원'], method = 'pearson')
    print("+++++",i,"& 축제인원과의 상관관계 분석+++++")
    print(corr)
    print("\n")