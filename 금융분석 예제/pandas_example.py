from pandas import Series
import pandas

# Series

obj = Series([4,7,-5,3])

print(obj)
print(obj.values)
print(obj.index)

# Series 인덱싱

obj2 = Series([4,7,5,3], index=['d','b','a','c'])
obj2

states = ['California','Ohio','Oregon','Texas']
obj2 = Series([1,3,5,7], index=states)
obj2

obj['a']
obj[['c','a','d']]

obj2[obj2 > 0]

obj2 * 2


# DataFrame

from pandas import DataFrame

data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
frame = DataFrame(data)
frame = DataFrame(data, columns=['year', 'state', 'pop'])  #컬럼 순서 지정
frame = DataFrame(data, columns=['year', 'state', 'pop', 'debt'])  # 'debt' 컬럼은 빈값(NaN)이 들어감
frame = DataFrame(data, columns=['year', 'state', 'pop', 'debt'],
                  index=['one', 'two', 'three', 'four', 'five'])  # dataframe도 인덱싱이 가능함

frame
frame['state']
frame.year


frame

frame['eastern'] = frame.state == 'Ohio'   # 없는 컬럼에 값을 대입하면 컬럼이 새로 생성됨
frame

del frame['eastern']  # 컬럼 삭제

