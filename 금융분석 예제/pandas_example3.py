import numpy as np
from pandas_datareader import data as web
import matplotlib.pyplot as plt
import math


DAX = web.DataReader('^GDAXI', data_source='yahoo', start='2010-1-1')

#print(DAX.info())
#print(DAX.tail())
#DAX['Close'].plot(figsize=(8,5))

#%%time
DAX['Ret_Loop'] = 0.0
for i in range(1, len(DAX)):        #반복문으로  연산하는 것
    DAX['Ret_Loop'][i] = np.log(DAX['Close'][i] /
    DAX['Close'][i-1])

print(DAX[['Close', 'Ret_Loop']].tail())

DAX['Return'] = np.log(DAX['Close'] / DAX['Close'].shift(1))    #반복문 없이 벡터연산, shift(1) 은 전체를 i - 1 만큼 미는 것과 같은 의미

#로그 수익률 차트
#DAX[['Close', 'Return']].plot(subplots=True, style='b', figsize=(8, 5))

#이동평균선
#DAX['42d'] = pd.rolling_mean(DAX['Close'], window=42)   #series는 rolling_mean()이 아닌 rolling().mean()으로 써야하는 것으로 바뀜
DAX['42d'] = DAX['Close'].rolling(window=42).mean()
DAX['252d'] = DAX['Close'].rolling(window=252).mean()

#DAX[['Close', '42d', '252d']].plot(figsize=(8, 5))

DAX['Mov_vol'] = DAX['Return'].rolling(window=252).std() * math.sqrt(252)

DAX[['Close', 'Mov_vol', 'Return']].plot(subplots=True, style='b', figsize=(8, 7))

# 플롯이 바로 나왔다가 닫히지 않게 하는 구문
plt.show()

#mpl.get_backend()
##