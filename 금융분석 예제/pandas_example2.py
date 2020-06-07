import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""기초 데이터프레임 생성 및 조인
df = pd.DataFrame([10,20,30,40], columns=['numbers'], index=['a','b','c','d'])
#print(df)

#print(df.ix[df.index[0:3]])

#print(df.apply(lambda x : x ** 2))   #apply는 계산식을 각 원소에 대해 적용하는 함수
#print(df ** 2)  # 벡터연산 가능

df['floats'] = (1.5, 2.5, 3.5, 4.5)   #floats라는 새로운 열 생성

df.append({'numbers': 500}, ignore_index=True) #새로 추가되는 것이 인덱스가 할당되지 않으면 임시로만 생성함, df에 추가안됨.

df.append(pd.DataFrame({'numbers': 100, 'floats': 5.75}, index=['z',])) # append 안에 dataframe을 통채로 넣으면 행이 추가됨

print(df)

df.join(pd.DataFrame([1,4,9,16,25], index=['a','b','c','d','y'], columns=['squares',])) # join은 index가 맞는 항목만 열로 붙여주는 기능
df.join(pd.DataFrame([1,4,9,16,25], index=['a','b','c','d','y'], columns=['squares',]), how='outer') # full outer 조인. inner, left, right 가능 , 디폴트는 left

"""
"""nparray에서 dataframe 생성 관련"""

a = np.random.standard_normal((9, 4))
a = a.round(6)

df = pd.DataFrame(a)
df.columns = [['No1', 'No2', 'No3', 'No4']]   #2차원 배열을 데이터프레임에 넣고 컬럼만 정해주면 알아서 들어감
#print(df)
#print(df['No2'][3])  #dataframe 값에 접근하는 방법

dates = pd.date_range('2015-1-1', periods=9, freq='MS')  #시작일, 개수, 주기를 입력해주면 알아서 월말 기준으로 날짜 생성 , 월초는 'MS'
#print(dates)

df.index = dates #인덱스를 dates로 설정

#print(np.array(df).round(6))  #dataframe을 nparray로 역변환

#print(df.sum()) #열 단위로 합계 # mean(), cumsum()

#print(df.describe()) #열 별로 데이터 summary 보여줌

#print(np.sqrt(df))  # numpy의 universal 함수는 dataframe에도 적용 가능

#df.cumsum().plot(lw=2.0)   #dataframe 객체의 plot 함수임



"""GrouopBy 연산"""

df['Quarter'] = ['Q1', 'Q1', 'Q1', 'Q2', 'Q2', 'Q2', 'Q3', 'Q3', 'Q3']
#print(df)
groups = df.groupby('Quarter')  #Quarter열 기준으로 그룹 객체를 만듬

print(groups.mean())
print(groups.max())
print(groups.size())

# 플롯이 바로 나왔다가 닫히지 않게 하는 구문
#plt.show()

#mpl.get_backend()
##