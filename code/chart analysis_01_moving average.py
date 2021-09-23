# 데이터 불러오기

import pandas as pd
import numpy as np
import time
import warnings

warnings.filterwarnings(action='ignore')


def read_data():
    print('종목 차트정보 가져오는 중...')
    dailychart = pd.read_csv('dailychart.csv')
    dailychart['date'] = pd.to_datetime(dailychart['date'], format='%Y%m%d')


    # 날짜 데이터프레임 생성
    df_date = pd.DataFrame(dailychart['date'].unique(), columns=['date'])
    min_day = np.min(dailychart['date'])
    max_day = np.max(dailychart['date'])
    df_date['idx'] = df_date.index

    dailychart = pd.merge(dailychart, df_date, on='date')

    print("종목정보 가져오는 중...")
    stockitems_original = pd.read_csv('stockItems.csv', encoding='cp949')   #종목정보 가져오기
    stockitems_in_chart = dailychart['code'].unique()
    stockitems = stockitems_original.loc[stockitems_original['code'].isin(stockitems_in_chart)]

    print("지수정보 가져오는 중...")
    dailychart_index = pd.read_csv('dailychart_index.csv', encoding='cp949')   #종목정보 가져오기
    dailychart_index['date'] = pd.to_datetime(dailychart_index['date'], format='%Y%m%d')
    dailychart_index = pd.merge(dailychart_index, df_date, on='date')
    dailychart_index = dailychart_index.loc[(min_day <= dailychart_index['date']) & ( dailychart_index['date'] <= max_day)]
    dailychart_index = dailychart_index.sort_values(['code','date']).reset_index(drop=True)

    # 각 종목별 시작일에 날짜 인덱스를 추가
    tmp_df = pd.merge(dailychart.groupby('code', as_index=False)['date'].min(), df_date, on='date' )

    # 종목 데이터에 종목별 시작일과 시작날짜 인덱스를 조인
    stockitems = pd.merge(stockitems_original, tmp_df, on='code')
    stockitems = stockitems.rename(columns = {'date':'firstdate', 'idx':'idx_firstdate'})

    pd.options.display.float_format = '{:.0f}'.format

    dailychart = dailychart.sort_values(['code','date']).reset_index(drop=True)

    print('데이터를 불러왔습니다.')

    return dailychart, dailychart_index, stockitems



def generate_rolling_mean(df, rolling_mean_period):
    for p in rolling_mean_period:
        column_name = 'rm_' + str(p)
        df[column_name + '_tmp'] = df['close'].rolling(p).mean().shift(-p + 1)
        df_groupby = df.groupby('code')[column_name + '_tmp'].shift(p - 1).rename(column_name)
        df = pd.concat([df, df_groupby], axis=1)
        df = df.drop(columns=column_name + '_tmp')
    return df


# 이평선 1. 골든크로스 (정배열)
def generate_reg_alignment(df):
    df['reg_alignment'] = False
    df.loc[
        (df['rm_5'] > df['rm_20']) & (df['rm_20'] > df['rm_60']) & (df['rm_60'] > df['rm_120']), 'reg_alignment'] = True
    df['golden_cross'] = False
    df.loc[(df['reg_alignment'] == True) & (df['reg_alignment'].shift(1) == False) & (
                df['code'] == df['code'].shift(1)), 'golden_cross'] = True
    return df


# 골든크로스 검증용 데이터 생성
def generate_val_data(df, period):
    idx_golden_cross = df.loc[df['golden_cross']].index
    arr_day = np.arange(0, period + 1)

    code = df.loc[idx_golden_cross, 'code']
    arr_gc_id = np.repeat(np.arange(0, len(idx_golden_cross)), period + 1)
    arr_code = np.repeat(code, period + 1)
    arr_day = np.tile(arr_day, len(code))

    idx_golden_cross = np.repeat(idx_golden_cross, period + 1) + arr_day
    arr = np.stack((idx_golden_cross, arr_gc_id, arr_code, arr_day), axis=-1)

    df_val_goldencross = pd.DataFrame(arr, columns=['index', 'gc_id', 'code', 'days']).set_index('index')

    return df_val_goldencross



######################## code ########################


# 데이터 불러오기
dailychart, dailychart_index, stockitems = read_data()


# 골든크로스 검색 및 검증 데이터 추출
rolling_mean_period = [5, 20, 60, 120]

dailychart_rolling = generate_rolling_mean(dailychart, rolling_mean_period)
dailychart_rolling = generate_reg_alignment(dailychart_rolling)
df_val_goldencross = generate_val_data(dailychart_rolling, 60)

df_val_goldencross = pd.merge(dailychart_rolling, df_val_goldencross, left_index=True, right_index=True)

df_val_goldencross = df_val_goldencross.loc[df_val_goldencross['code_x'] == df_val_goldencross['code_y'],
                                            ['gc_id', 'days', 'code_x', 'section', 'date', 'close', 'vol', 'rm_5',
                                             'rm_20', 'rm_60', 'rm_120', 'reg_alignment']]

# 인덱스일 경우
# df_val_goldencross = df_val_goldencross.loc[df_val_goldencross['code_x'] == df_val_goldencross['code_y'],
#                                            ['gc_id', 'days', 'code_x', 'section', 'date', 'close', 'rm_5', 'rm_20','rm_60','rm_120', 'reg_alignment']]

df_val_goldencross = df_val_goldencross.rename(columns={'code_x': 'code'})

df_val_goldencross = df_val_goldencross.sort_values(['gc_id', 'days'])

df_val_goldencross.to_csv('val_goldencross.csv', index=False)


# 골든크로스 수익률 통계

df = pd.read_csv('val_goldencross.csv')
df_index = pd.read_csv('val_goldencross_index.csv')
df['date'] = pd.to_datetime(df['date'])
df_index['date'] = pd.to_datetime(df_index['date'])

pd.options.display.float_format = '{:,.2f}'.format

df['close'] = df['close'].astype(float)
df['ret_day'] = (df['close']-df['close'].shift(1)) / df['close'].shift(1) * 100
df.loc[df['days'] == 0, 'ret_day'] = np.nan

df['ret_first'] = df.groupby('gc_id').close.transform('first')
df['ret_first'] = (df['close'] - df['ret_first']) / df['ret_first'] * 100


# 골든크로스 발생일로부터 d일 후의 수익률 평균

# 1. 모든 케이스에 대한 평균

df_summary = df.groupby('days')['ret_day', 'ret_first'].mean()
df_summary[['std_ret_day', 'std_ret_first']] = df.groupby('days')['ret_day', 'ret_first'].std()


# 2. 골드크로스 발생일로부터 120영업일 이내 재발생된 골드크로스 제외
df_first = df.loc[df['days'] == 0]

df_date = pd.DataFrame(dailychart['date'].unique(), columns =['date'])
df_date = df_date.reset_index()
df_date = df_date.rename(columns={'index':'idx'})

df_first = pd.merge(df_first, df_date, left_on='date',right_on='date')
df_first = df_first.sort_values('gc_id')
df_first = df_first.loc[ ~((df_first['idx'] - df_first.shift(1)['idx'] <= 120) & (df_first['code'] == df_first.shift(1)['code']))]

df = df.loc[df['gc_id'].isin(df_first['gc_id'])]

df_summary = df.groupby('days')['ret_day', 'ret_first'].mean()
df_summary[['std_ret_day', 'std_ret_first']] = df.groupby('days')['ret_day', 'ret_first'].std()

df_summary








# 120일 선이 하락추세일 때  상승하지 않음
#df.loc[df['gc_id'] == 4, 'close'].plot()


df.loc[df['gc_id'] == 8, 'close'].plot()
df.loc[df['gc_id'] == 8, ['rm_5','rm_20','rm_60','rm_120']].plot()

"""
# 2014년 이후 코스탁 → 코스피 이전 상장 기업 주요 기업

한국토지신탁(2016.7.11), 카카오(2017.7.10), 셀트리온(2018,2,9), 더블유게임즈(2019.3.12),  포스코케미칼(2019,5,29)


# 2014년 이후 코스피200 종목 변경일
2014. 6. 13
2015. 6. 12
2016. 6. 10
2017. 6. 9
2018. 6. 15
2019. 6. 14
2020. 6. 12
2020.12.11
2021. 6. 11


# 코스닥150 종목 변경일 (2015년 7월 13일 최초 생성 및 이후)
2015. 7. 13
2015. 12. 11
2016. 6. 10
2016. 12. 9
2017. 6. 9
2017. 12. 15
2018. 6. 15
2018. 12. 14
2019. 6. 14
2019. 12. 13
2020. 6. 12
2020.12.11
2021. 6. 11
