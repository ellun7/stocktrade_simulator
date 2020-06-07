import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
from sklearn.decomposition import KernelPCA
yf.pdr_override()
import matplotlib.pyplot as plt
import matplotlib as mpl



symbols = ['ADS.DE', 'ALV.DE', 'BAS.DE', 'BAYN.DE', 'BEI.DE',
           'BMW.DE', 'CBK.DE', 'CON.DE', 'DAI.DE', 'DB1.DE',
           'DBK.DE', 'DPW.DE', 'DTE.DE', 'EOAN.DE', 'FME.DE',
           'FRE.DE', 'HEI.DE', 'HEN3.DE', 'IFX.DE', 'LHA.DE',
           'LIN.DE', 'LXS.DE', 'MRK.DE', 'MUV2.DE', 'RWE.DE',
           'SAP.DE', 'SDF.DE', 'SIE.DE', 'TKA.DE', 'VOW3.DE',
           '^GDAXI']

data = pd.DataFrame()
for sym in symbols:
    data[sym] = pdr.get_data_yahoo(sym, data_source='yahoo', start='2010-4-1')['Adj Close']
data = data.dropna()

dax = pd.DataFrame(data.pop('^GDAXI'))

#print(data[data.columns[:6]].head)

scale_function = lambda x: (x - x.mean()) / x.std()   #정규분포 내에서 상대적 위치를 반환
get_we = lambda x: x / x.sum()    #합을 1로 정규화하는 함수

# 최대 개수로 주성분 분석
"""
pca = KernelPCA().fit(data.apply(scale_function))   #주성분 분석 실시

print(len(pca.lambdas_))
print(pca.lambdas_[:10].round())

print(get_we(pca.lambdas_)[:10])
print(get_we(pca.lambdas_)[:10].sum())   # 가장 비중이 큰 10개의 주성분만으로 97%를 설명가능
"""

# 한 개 주성분이 나오도록 분석
pca = KernelPCA(n_components=1).fit(data.apply(scale_function))
dax['PCA_1'] = pca.transform(data)    # 주성분을 기준으로 data를 재구성

# 두 개 주성분이 나오도록 분석
#pca2 = KernelPCA(n_components=2).fit(data.apply(scale_function))
#pca_components = pca.transform(data)
#weights = get_we(pca.lambdas_)  #다섯 개의 주성분 비중을 정규화
#dax['PCA_2'] = np.dot(pca_components, weights)  #가중평균으로 계산

# 다섯 개 주성분이 나오도록 분석
pca = KernelPCA(n_components=5).fit(data.apply(scale_function))
pca_components = pca.transform(data)
weights = get_we(pca.lambdas_)  #다섯 개의 주성분 비중을 정규화
dax['PCA_5'] = np.dot(pca_components, weights)  #가중평균으로 계산

#dax.apply(scale_function).plot(figsize=(8, 4))


mpl_dates = mpl.dates.date2num(data.index.to_pydatetime())

plt.figure(figsize=(8,4))
plt.scatter(dax['PCA_5'], dax['^GDAXI'], c=mpl_dates, s=np.repeat(6, len(dax)))
lin_reg = np.polyval(np.polyfit(dax['PCA_5'], dax['^GDAXI'], 1), dax['PCA_5'])
plt.plot(dax['PCA_5'], lin_reg, 'r', lw=3)
plt.grid(True)
plt.xlabel('PCA_5')
plt.ylabel('^GDAXI')
plt.colorbar(ticks=mpl.dates.DayLocator(interval=250),
             format=mpl.dates.DateFormatter('%d %b %y'))

# 각각의 연결된 선 하나가 하나의 회귀모형으로 최대한 만족할 수 있는 구간으로 해석

cut_date = '2011/7/1'
early_pca = dax[dax.index < cut_date]['PCA_5']
print(len(early_pca))
print(len(dax['^GDAXI'][dax.index < cut_date]))
early_reg = np.polyval(np.polyfit(early_pca, dax['^GDAXI'][dax.index < cut_date], 1), early_pca)

cut_date2 = '2015/6/1'
#middle_pca = np.where(dax.index >= cut_date and dax.index < cut_date2)['PCA_5']
#middle_pca = dax[dax.index >= cut_date]['PCA_5'] & dax[dax.index < cut_date2]['PCA_5']
middle_pca = dax[np.logical_and(dax.index >= cut_date, dax.index < cut_date2)]['PCA_5']
  #middle_gdaxi = dax[dax.index >= cut_date]['^GDAXI'] & dax[dax.index < cut_date2]['^GDAXI']
middle_gdaxi = dax[np.logical_and(dax.index >= cut_date, dax.index < cut_date2)]['^GDAXI']
#print(len(middle_pca))
#print(len(middle_gdaxi))
middle_reg = np.polyval(np.polyfit(middle_pca, middle_gdaxi, 1), middle_pca)

late_pca = dax[dax.index >= cut_date2]['PCA_5']
late_reg = np.polyval(np.polyfit(late_pca, dax['^GDAXI'][dax.index >= cut_date2], 1), late_pca)

plt.figure(figsize=(8,4))
plt.scatter(dax['PCA_5'], dax['^GDAXI'], c=mpl_dates, s=np.repeat(6, len(dax)))
plt.plot(early_pca, early_reg, 'r', lw=3)
plt.plot(middle_pca, middle_reg, 'r', lw=3)
plt.plot(late_pca, late_reg, 'r', lw=3)
plt.grid(True)
plt.xlabel('PCA_5')
plt.ylabel('^GDAXI')
plt.colorbar(ticks=mpl.dates.DayLocator(interval=250),
             format=mpl.dates.DateFormatter('%d %b %y'))

plt.show()

