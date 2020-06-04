#회귀분석
#정규화 방문객 pandas dataframe 만들기
import numpy as np
import pandas as pd

festival_df = pd.read_excel('통합축제데이터.xlsx', header = 0, sheet_name = 'Sheet1')
#있는 것 만으로 감정분석
sentiment = festival_df.dropna(axis=0)

#데이터 셋 분리하기
from sklearn.model_selection import train_test_split
x = sentiment[['년도', '축제명', '기간', "KTX역",'평균기온 절대값', '최저기온 절대값', '최고기온 절대값','평균운량', 'positive', 'neutral', '평균방문객']]
y = sentiment[['합계']]


x_train_split, x_test_split, y_train, y_test = train_test_split(x,y, train_size =0.8, test_size= 0.2)
x_train = x_train_split[['기간', "KTX역",'평균기온 절대값', '최저기온 절대값', '최고기온 절대값','평균운량', 'positive', 'neutral', '평균방문객']]
x_test = x_test_split[['기간', "KTX역",'평균기온 절대값', '최저기온 절대값', '최고기온 절대값','평균운량', 'positive', 'neutral', '평균방문객']]

#모델 생성하기

from sklearn.linear_model import LinearRegression
mlr= LinearRegression()
mlr.fit(x_train, y_train)

#예측하기
# 맞추먄 잘 맞출 수록 선으로 일치되어 나올 것이다.
import matplotlib.pyplot as plt
y_predict = mlr.predict(x_test)


plt.scatter(y_test, y_predict, alpha=0.4)
plt.xlabel("Actual visitor")
plt.ylabel("Predicted visitor")
plt.title("MULTIPLE LINEAR REGRESSION")
plt.show()

print("훈련세트점수: {}".format(mlr.score(x_train, y_train)))
print("테스트세트점수: {}".format(mlr.score(x_test, y_test)))

from sklearn.metrics import explained_variance_score, mean_squared_error, mean_absolute_error, r2_score
print('explained_variance_score: {}'.format(explained_variance_score(y_test, y_predict)))
print('mean_squared_errors: {}'.format(mean_squared_error(y_test, y_predict)))
print('r2_score: {}'.format(r2_score(y_test, y_predict)))