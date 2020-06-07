import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
##%matplotlib inline

np.random.seed(1000)
y = np.random.standard_normal(20)


""" 기본 꺾은선 차트 예제
#plt.interactive(True)
x = range(len(y))    #len()은 항목의 개수 반환
#plt.plot(x,y) #x, y 좌표에 해당하는 값을 매칭해서 꺾은선으로 뿌려줌
#plt.plot(y) #ndarray 객체이면 자동으로 x축을 1,2,3,4 순서로 매겨줌


z = y.cumsum() # cumsum() 순서대로 누적합을 구함
plt.plot(z)
plt.grid(True)
plt.xlim(-1,20)
plt.ylim(np.min(y.cumsum())-1, np.max(y.cumsum())+1)
#plt.axis('tight')

"""
""" 스캐터 플롯 예제1
y = np.random.standard_normal((1000,2))  #1000개 normal distribution을 2개 생성(2차원 행렬)

plt.figure(figsize=(7, 5))
plt.plot(y[1:1000, 0], y[:, 1], 'ro')  # : 와 1:1000 은 동일(전체를 의미), 0, 1은 2차원 배열 요소 1000 x 2 행렬
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')
"""

""" 스캐터 플롯 예제2
y = np.random.standard_normal((1000,2))  #1000개 normal distribution을 2개 생성(2차원 행렬)

plt.figure(figsize=(7, 5))
plt.scatter(y[:, 0], y[:, 1], marker='o')
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')
"""

""" 스캐터 플롯 예제3(컬러 마커로 3차원 추가 가능)
y = np.random.standard_normal((1000,2))
c = np.random.randint(0, 10, len(y))

plt.figure(figsize=(7, 5))
plt.scatter(y[:, 0], y[:, 1], c=c, marker='o')
plt.colorbar()
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')
"""

""" 히스토그램
y = np.random.standard_normal((1000,2))

plt.figure(figsize=(7, 4))
plt.hist(y, label=['1st','2nd'], color=['b','g'], bins=20, stacked=True)
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('value')
plt.ylabel('frequency')
plt.title('Histogram')
"""

""" 박스플롯 """
y = np.random.standard_normal((1000,2))

fig, ax = plt.subplots(figsize=(7, 4))   #입력값에 ,가 있으면 반환값이 2개일 때 차례대로 두 개 변수에 값이 들어감, fig는 전체 플롯, ax는 서브플롯
plt.boxplot(y)
plt.grid(True)
plt.setp(ax, xticklabels=['1st', '2nd'])  #플롯 객체의 속성을 설정, 플롯 객체 자체에 속성을 부여하거나 변경할 수 있음
plt.xlabel('data set')
plt.ylabel('value')
plt.title('Boxplot')



# 플롯이 바로 나왔다가 닫히지 않게 하는 구문
plt.show()
#mpl.get_backend()
##