import numpy as np
import matplotlib.pyplot as plt
import matplotlib.finance as mpf  #pyploy과 라이브러리가 다름

from pandas_datareader import data as web  #from으로 가져오면 함수쓸 때 앞에 라이브러리명을 안붙여도 됨




start = '2014-05-01'
end = '2014-06-30'
"""첫번째 예제

#독일 지수값 가져오기
df = web.DataReader('^GDAXI', data_source='yahoo', start=start, end=end)
df = df.reset_index()
df["Date"] = df["Date"].apply(lambda x: x.toordinal())  #날짜를 0,1,2,3 순서로 서수화 시킴
quotes = [tuple(x) for x in df.to_records(index=False)]  #Epoch 시간형식, 시가, 종가, 고가, 저가 순서

print(df[:2])
print(quotes[:2])

fig, ax = plt.subplots(figsize=(8,5))
fig.subplots_adjust(bottom=0.2)
mpf.candlestick_ohlc(ax, quotes[:10], width=0.6, colorup='b', colordown='r') #수익률이 양수인 경우 파란색, 음수인 경우 빨간색
plt.grid(True)
ax.xaxis_date()
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=30) #x축 레이블을 30도 회전시킴

#plt.gca()는 현재 figure객체를 반환

"""


df = web.DataReader('^GDAXI', data_source='yahoo', start=start, end=end)
df = df.reset_index()
df["Date"] = df["Date"].apply(lambda x: x.toordinal())  #날짜를 0,1,2,3 순서로 서수화 시킴
quotes = [tuple(x) for x in df.to_records(index=False)]  #Epoch 시간형식, 시가, 종가, 고가, 저가 순서
quotes = np.array(quotes)

fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(8, 6))
mpf.candlestick_ohlc(ax1, quotes, width=0.6, colorup='b', colordown='r') #수익률이 양수인 경우 파란색, 음수인 경우 빨간색
ax1.set_title('Yahoo Inc.')
ax1.set_ylabel('index label')
ax1.grid(True)
ax1.xaxis_date()

plt.bar(quotes[:,0] - 0.25, quotes[:,5], width=0.5)
ax2.set_ylabel('volume')
ax2.grid(True)
ax2.set_ylim([9000, 10500])
ax2.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=30) #x축 레이블을 30도 회전시킴

# 플롯이 바로 나왔다가 닫히지 않게 하는 구문
plt.show()
##