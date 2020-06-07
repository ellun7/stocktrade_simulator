import numpy as np
import pandas as pd
from pandas_datareader import data as web
import matplotlib.pyplot as plt
import scipy.optimize as sco
import scipy.interpolate as sci

def statistics(weights):
    weights = np.array(weights)
    pret = np.sum(np.sum(rets.mean() * weights) * 252)   # 연수익률
    pvol = np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))   # 연 공분산
    return np.array([pret, pvol, pret / pvol])   # 연수익률, 연 공분산, 샤프지수

def min_func_sharpe(weights):
    return -statistics(weights)[2]

def min_func_variance(weights):
    return statistics(weights)[1] ** 2

#symbols = ['AMZN', 'MSFT', 'AABA', 'DB', 'GLD']
symbols = ['AMZN','MSFT', 'AABA']
data = pd.DataFrame()
#data = web.DataReader('078930.KS', 'yahoo', start='2017-4-1')['Close']
for sym in symbols:
    data[sym] = web.DataReader(sym, data_source='google', start='2015-4-1', end='2016-4-1')['Close']
data.columns = symbols

#(data / data.ix[0] * 100).plot(figsize=(8, 5))   #data.ix[0] 은 각 종목의 기준일 첫째날 주가

rets = np.log(data / data.shift(1))  #로그 수익률

#print(rets.mean() * 252) # 연 수익률
#print(rets.cov() * 252) # 연 공분산 행렬


###

noa = len(symbols)
weights = np.random.random(noa)
weights /= np.sum(weights)

np.sum(rets.mean() * weights) * 252  # 임의 가중치를 가지는 포트폴리오의 연 수익률

portfolio_var = np.dot(weights.T, np.dot(rets.cov() * 252, weights))  # 포트폴리오의 분산 기댓값
portfolio_std = np.sqrt(portfolio_var)
#print("Std of Portfolio : ")
#print(portfolio_std)

prets = []
pvols = []
for p in range (2500):                    #몬테카를로 시뮬레이션으로 2500개 샘플 추출
    weights = np.random.random(noa)        #random의 매개변수는 랜덤숫자를 만드는 개수. 길이 3의 array 생성
    weights /= np.sum(weights)             #랜덤 숫자의 총합을 1로 정규화
    prets.append(np.sum(rets.mean() * weights) * 252)                                 #임의 가중치로 테스트한 포트폴리오 연 수익률
    pvols.append(np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights))))       #임의 가중치로 테스트한 포트폴리오 연 표준편차의 기댓값

prets = np.array(prets)
pvols = np.array(pvols)
#print(np.repeat(6, len(prets)))
plt.figure(figsize=(8, 4))
plt.scatter(pvols, prets, c=prets / pvols, marker='o', s=np.repeat(6, len(prets)))    # 무위험 단기 이자율이 r인 경우 샤프지수는  (prets - r) / pvols 임
plt.grid(True)
plt.xlabel('expected volatiiity')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')


cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bnds = tuple((0, 1) for x in range(noa))

opts = sco.minimize(min_func_sharpe, noa * [1. / noa], method='SLSQP', bounds=bnds, constraints=cons)   #샤프지수 최대화 포트폴리오 최적화

print(opts)   # x 값이 목표한 최적해임

optv = sco.minimize(min_func_variance, noa * [1. / noa], method='SLSQP', bounds=bnds, constraints=cons)   #공분산 최소화 포트폴리오 최적화

##### 효율적 투자선 구하기

def min_func_port(weights):
    return statistics(weights)[1]

cons = ({'type': 'eq', 'fun': lambda x: statistics(x)[0] - tret},
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bnds = tuple((0,1) for x in weights)

trets = np.linspace(0.45, 0.60, 50)
tvols = []
for tret in trets:   # 각 수익률 별로 최소 공분산을 갖는 투자비중을 계산
    cons = ({'type': 'eq', 'fun': lambda x: statistics(x)[0] - tret},
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    res = sco.minimize(min_func_port, noa * [1. / noa,], method='SLSQP', bounds=bnds, constraints=cons)
    tvols.append(res['fun'])
tvols = np.array(tvols)

print(tvols)

plt.figure(figsize=(8, 4))
plt.scatter(pvols, prets, c=prets / pvols, marker='o')  #무작위 포트폴리오
#plt.scatter(tvols, trets, c=trets/tvols, marker='x') #효율적 투자선
plt.plot(statistics(opts['x'])[1], statistics(opts['x'])[0], 'r*', markersize=6.0)  # 최대 샤프지수 포트폴리오
plt.plot(statistics(optv['x'])[1], statistics(optv['x'])[0], 'y*', markersize=6.0)   # 최소분산 포트폴리오

plt.grid(True)
plt.xlabel('expected volatility')
plt.ylabel('exptected return')
plt.colorbar(label='Sharpe ratio')



ind = np.argmin(tvols)   # 공분산이 가장 작은 인덱스를 추출
evols = tvols[ind:]
erets = trets[ind:]      #공분산이 가장 작은 인덱스 부터의 집합을 생성

tck = sci.splrep(evols, erets, k=3)    #각 점들을 연결할 수 있도록 보간법 사용
#tck[0] = tck[0][:len(tck[0])-3]
#tck[1] = tck[1][:len(tck[1])-3]

evols2 = tck[0][:len(tck[0])-4]
erets2 = tck[1][:len(tck[1])-4]


def f(x):
    return sci.splev(x, tck, der=0)

def df(x):
    return sci.splev(x, tck, der=1)

def equations(p, rf=0.01):
    eq1 = rf - p[0]
    eq2 = rf + p[1] * p[2] - f(p[2])
    eq3 = p[1] - df(p[2])
    return eq1, eq2, eq3

opt = sco.fsolve(equations, [0.01, 0.5, 0.15])

print(opt)

np.round(equations(opt), 6)

plt.figure(figsize=(8, 4))
plt.plot(evols, erets) #효율적 투자선
plt.plot(evols2, erets2) #효율적 투자선
plt.scatter(pvols, prets, c=(prets - 0.01) / pvols, marker='o') # 무작위 투자선
#plt.scatter(evols, erets, 'g', lw=4.0)    # 효율적 투자선
cx = np.linspace(0.14, 0.24)
plt.plot(cx, opt[0] + opt[1] * cx, lw=1.5)  # 자본시장선
plt.plot(opt[2], f(opt[2]), 'r*', markersize=6.0)
plt.grid(True)
#plt.axhline(0, color='k', li='--', lw=2.0)
#plt.axvline(0, color='k', ls='--', lw=2.0)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')

cons = ({'type':'eq', 'fun': lambda x: statistics(x)[0]- f(opt[2])},
        {'type':'eq', 'fun': lambda x: np.sum(x) - 1})
res = sco.minimize(min_func_port, noa * [1. / noa, ], method='SLSQP', bounds=bnds, constraints=cons)

print(res['x'].round(3))


plt.show()


