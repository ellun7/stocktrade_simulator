from pandas_datareader import data as web
import matplotlib.pyplot as plt

DAX = web.DataReader('^GDAXI', data_source='yahoo', start='2010-1-1')
#df = web.DataReader('^GDAXI', data_source='yahoo', start=start, end=end)
DAX.info() #객체 형식 확인 dataframe임

print(DAX.tail())  #데이터의 마지막 5열을 보여줌

DAX['Close'].plot(figsize=(8,5))


# 플롯이 바로 나왔다가 닫히지 않게 하는 구문
plt.show()
##