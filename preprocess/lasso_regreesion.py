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

from sklearn.linear_model import Lasso
lasso = Lasso().fit(x_train, y_train)
print("훈련세트점수: {}".format(lasso.score(x_train, y_train)))
print("테스트세트점수: {}".format(lasso.score(x_test, y_test)))
print("사용한 특성의 수:", (np.sum(lasso.coef_ != 0)))


#최소 적합 해결
lasso001 = Lasso(alpha = 0.1, max_iter = 100000).fit(x_train, y_train)
print("훈련세트점수: {}".format(lasso001.score(x_train, y_train)))
print("테스트세트점수: {}".format(lasso001.score(x_test, y_test)))
print("사용한 특성의 수:", (np.sum(lasso.coef_ != 0)))

#최소 적합 해결
lasso00001 = Lasso(alpha = 0.0001, max_iter = 100000).fit(x_train, y_train)
print("훈련세트점수: {}".format(lasso00001.score(x_train, y_train)))
print("테스트세트점수: {}".format(lasso00001.score(x_test, y_test)))
print("사용한 특성의 수:", (np.sum(lasso.coef_ != 0)))