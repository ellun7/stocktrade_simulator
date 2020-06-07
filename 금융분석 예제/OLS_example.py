import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

from urllib.request import urlretrieve     #url주소로 자료 받을 수 있는 라이브러리

es_url = 'http://www.stoxx.com/download/historical_values/hbrbcpe.txt'
vs_url = 'http://www.stoxx.com/download/historical_values/h_vstoxx.txt'
#urlretrieve(es_url, './data/es.txt')   #url주소로 있는 데이터를 가지고 올 수 있는 함수
#urlretrieve(vs_url, './data/vs.txt')


#Raw데이터를 dataframe으로 만드는 방법 1 (데이터를 파싱하여 리스트에 넣고 데이터프레임으로 변환)

#데이터 전처리
lines = open('C:/Users/user/PycharmProjects/untitled2/금융분석 예제/data/es.txt', 'r').readlines()
#lines = [line.replace(' ', '') for line in lines]    #리스트 내포   [ 표현식 for  매개변수 in 반복가능객체 if 조건 ]
lines = [line.replace(' ', '') for line in lines]

#print(lines[:6])

#for line in lines[3883:3890]:
    #print(line[41:])

# 파일 다시 쓰기

new_file = open('./data/es50.txt', 'w')
new_file.writelines('date' + lines[3][:-1] + ';DEL' + lines[3][-1])   #줄 끝의 세미콜론을 잡기 위해 편의상 DEL이라는 보조열 추가
new_file.writelines(lines[4:])
new_file.close()

new_lines = open('./data/es50.txt', 'r').readlines()
#print(new_lines[:5])

#텍스트를 pandas 객체로 생성
es = pd.read_csv('./data/es50.txt', index_col=0, parse_dates=True, sep=';', dayfirst=True)
#print(es.tail())
#print(np.round(es.tail()))    #np.round( )  괄호안에 있는 숫자를 정수로 만듬

#del es['DEL']
#es.info()


#Raw데이터를 dataframe으로 만드는 방법 2  (원시데이터가 구분자로 구별되어 있으면 바로 읽어오기 가능)

cols = ['SX5P', 'SX5E', 'SXXP', 'SXXE', 'SXXF', 'SXXA', 'DK5F', 'DKXF']
es = pd.read_csv('./data/es.txt', index_col=0, parse_dates=True, sep=';', dayfirst=True, header=None, skiprows=4, names=cols)

vs = pd.read_csv('./data/vs.txt', index_col=0, parse_dates=True, sep=',', dayfirst=True, header=2)

#print(es.tail())
#print(vs.tail())

#날짜를 기준으로 EUROSTOXX의 SX5E와 VSTOXX의 V2TX를 조인
data = pd.DataFrame({'EUROSTOXX' :
                     es['SX5E'][es.index > dt.datetime(1999, 1, 1)]})
data = data.join(pd.DataFrame({'VSTOXX' : vs['V2TX'][vs.index > dt.datetime(1999, 1, 1)]}))
data = data[data.index < '2014-09-27']

data = data.fillna(method='ffill')    #'ffill' : forward fill,  'bfill' : backward fill
print(data.tail())


#data.plot(subplots=True, grid=True, style='b', figsize=(8,6))





#로그 수익률 구하기

rets = np.log(data / data.shift(1))   #전날 대비 오늘 로그 수익률
rets.dropna(inplace=True)
#rets.plot(subplots=True, grid=True, style='b', figsize=(8,6))

#plt.show()


#유로스톡스50 수익률은 독립변수, VSTOXX수익률은 종속변수로 하는 OLS 분석

xdat = rets['EUROSTOXX'].values
ydat = rets['VSTOXX'].values
reg = np.polyfit(x=xdat, y=ydat, deg=1)   #다중회귀

print(reg)
#첫번째 항 : 기울기, 두번째 항 : y절편


#분석결과 시각화

#plt.plot(xdat, ydat, 'r.')   #산점도
ax = plt.axis()
x = np.linspace(ax[0], ax[1] + 0.01)
#plt.plot(x, reg[1]+ reg[0] * x, 'b', lw=2)   #plot에 수식에 해당하는 그래프 추가
#plt.grid(True)
#plt.axis('tight')
#plt.xlabel('EURO STOXX 50 returns')
#plt.ylabel('VSTOXX returns')


#plt.show()


#상관계수 시각화

rets.corr()

rets['EUROSTOXX'].rolling(window=252).corr(rets['VSTOXX']).plot(grid=True, style='b')
#rolling_corr(rets['EUROSTOXX'], rets['VSTOXX'], window=252).plot(grid=True, style='b')

plt.show()