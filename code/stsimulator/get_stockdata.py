# 대신증권 Cybos API 기반의 종목리스트 및 일일 주가 데이터 가져와서 csv 파일로 저장합니다.


import win32com.client
import pandas as pd
import time
import datetime
import pickle
import os

parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

path_data = parent_path + '/data/'
column_stockitem = ['code', 'name', 'section', 'sectionKind']
column_dailychart = ['code', 'section', 'date', 'open', 'high', 'low', 'close',
                     'vol', 'value', 'n_stock', 'agg_price', 'foreign_rate', 'agency_buy']

print ('aaa')

CPE_MARKET_KIND = {'KOSPI': 1, 'KOSDAQ': 2}


def get_stockitem():
    CPE_MARKET_KIND = {'KOSPI': 1, 'KOSDAQ': 2}

    instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

    rows = list()

    for key, value in CPE_MARKET_KIND.items():
        codeList = instCpCodeMgr.GetStockListByMarket(value)
        for code in codeList:
            name = instCpCodeMgr.CodeToName(code)
            sectionKind = instCpCodeMgr.GetStockSectionKind(code)
            row = [code, name, key, sectionKind]
            rows.append(row)

    stockitems = pd.DataFrame(data=rows, columns=['code', 'name', 'section', 'sectionKind'])
    stockitems.loc[stockitems['sectionKind'] == 10, 'section'] = 'ETF'

    print('모든 종목을 불러왔습니다')

    return stockitems


def get_stockdata(stockitems, fromdate, enddate):
    instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    nCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")

    row = list(range(len(column_dailychart)))
    rows = list()

    instStockChart.SetInputValue(1, ord('1'))
    # instStockChart.SetInputValue(2, (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
    instStockChart.SetInputValue(2, enddate)
    instStockChart.SetInputValue(3, fromdate)
    instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8, 9, 12, 13, 17, 20))
    instStockChart.SetInputValue(6, ord('D'))
    instStockChart.SetInputValue(9, ord('1'))

    j = 0
    for idx, stockitem in stockitems.iterrows():

        if j >= 10:
            break

        remain_request_count = nCpCybos.GetLimitRemainCount(1)
        print(stockitem['code'], stockitem['name'], '남은 요청 : ', remain_request_count)

        if remain_request_count == 0:
            print('남은 요청이 모두 소진되었습니다. 잠시 대기합니다.')

            while True:
                time.sleep(2)
                remain_request_count = nCpCybos.GetLimitRemainCount(1)
                if remain_request_count > 0:
                    print('작업을 재개합니다. (남은 요청 : {0})'.format(remain_request_count))
                    break
                print('대기 중...')

        instStockChart.SetInputValue(0, stockitem['code'])

        # BlockRequest
        instStockChart.BlockRequest()

        # GetHeaderValue
        numData = instStockChart.GetHeaderValue(3)
        numField = instStockChart.GetHeaderValue(1)

        # GetDataValue
        for i in range(numData):
            row[0] = stockitem['code']
            row[1] = stockitem['section']  # 코스피, 코스닥, ETF 여부
            row[2] = instStockChart.GetDataValue(0, i)  # 날짜 / date
            row[3] = instStockChart.GetDataValue(1, i)  # 시가 / open
            row[4] = instStockChart.GetDataValue(2, i)  # 고가 / high
            row[5] = instStockChart.GetDataValue(3, i)  # 저가 / low
            row[6] = instStockChart.GetDataValue(4, i)  # 종가 / close
            row[7] = instStockChart.GetDataValue(5, i)  # 거래량 / vol
            row[8] = instStockChart.GetDataValue(6, i) / 1000000  # 거래대금(백만원) / value
            row[9] = instStockChart.GetDataValue(7, i)  # 상장주식수 / n_stock
            row[10] = instStockChart.GetDataValue(8, i) / 1000000  # 시가총액 / agg_price
            row[11] = instStockChart.GetDataValue(9, i)  # 외국인 보율비율 / foreign_rate
            row[12] = instStockChart.GetDataValue(10, i)  # 기관순매수 / agency_buy
            rows.append(list(row))  # 그냥 row를 입력하면 그 전에 입력되었던 row까지 다 현재 값으로 바뀜

        j += 1

    print('데이터를 모두 불러왔습니다.')

    return rows


def update_data(df_prev, df):
    # data-rows 간 길이 일치 여부 검사
    if not df_prev.columns.tolist() == df.columns.tolist():
        print('data와 rows 간 column이 일치하지 않습니다.')
        return

    df = df_prev.append(df)
    if 'date' in df_prev.columns.tolist():
        df = df.drop_duplicates(subset=['code', 'date'])
    else:
        df = df.drop_duplicates(subset=['code'])

    print('데이터를 업데이트하였습니다.')
    return df


def save_by_split(rows):
    # 2년 이상 큰 데이터를 저장할 때는 파일을 쪼개서 저장 후 64bit 버전에서 합쳐서 저장
    # dailychart = pd.DataFrame(data = rows, columns= column_dailychart)
    # MemoryError: Unable to allocate 190. MiB for an array with shape (3554329, 14) and data type object
    # 32bit로 실행할 경우 큰 데이터를 pandas dataframe으로 옮기는 과정에서 위와같은 에러가 발생

    unit = 500000

    i = 0
    for i in range(0, int(len(rows) / unit)):
        with open(path_data + 'tmp_dailychart{0}.dat'.format(i), 'wb') as f:
            pickle.dump(rows[i * unit:(i + 1) * unit], f)

    if i > 0:
        i += 1
    with open(path_data + 'tmp_dailychart{0}.dat'.format(i), 'wb') as f:
        pickle.dump(rows[(i) * unit:len(rows)], f)

    print('임시 데이터를 분할 저장하였습니다.')


def merge_splitedfiles(n_file):
    ## 분할저장한 주가정보파일 합치기

    data = list()

    for i in range(0, n_file):
        with open(path_data + 'tmp_dailychart{0}.dat'.format(i), 'rb') as f:
            tmp_data = pickle.load(f)
        data = data + tmp_data

    print('임시 데이터를 합치기를 완료하였습니다.')

    return data





