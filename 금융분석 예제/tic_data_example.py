import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

url1 = 'http://hopey.netfonds.no/posdump.php?'
url2 = 'date=%s%s%s&paper=GE.N&csv_format=csv'
url = url1 + url2

year = '2017'
month = '12'
days = ['27','28','29']

NKE = pd.DataFrame()
for day in days :
    NKE = NKE.append(pd.read_csv(url % (year, month, day), index_col=0, header=0, parse_dates=True))   #url 내의 매개변수를 지정할 수 있음

NKE.columns = ['bid', 'bdepth', 'bdeptht', 'offer', 'odepth', 'odeptht']

NKE.info()

#NKE['bid'].plot(grid=True)

# 틱 데이터와 거래량 차트로 표시

#to_plot = NKE[['bid', 'bid_depth_total']][
#    (NKE.index > dt.datetime(2017, 12, 27, 15, 0))
#    & (NKE.index < dt.datetime(2017, 12, 28, 9, 0))]
#to_plot.plot(subplots=True, style='b', figsize=(8,5), grid=True)


# 틱 데이터를 시간간격으로 리샘플링

NKE_resam = NKE.resample(rule='5min').mean()
np.round(NKE_resam.head(), 2)
NKE_resam['bid'].fillna(method='ffill').plot(grid=True)
#plt.show()

def reversal(x):
    return 2 * 95 - x

NKE_resam['bid'].fillna(method='ffill').apply(reversal).plot(grid=True)  # apply(function) series를 reversal 함수에 적용함.   fillna 는 결측값만 특정값으로 대체

plt.show()