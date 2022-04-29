import sys, json, requests
import pandas as pd

session = requests.Session()
session.verify = False

host_url = 'https://checkapi.koscom.co.kr'

# 0. 로그인 정보
id = ''
api = ''


# 1. 대상 api 정보
ks_code_info = '/stock/m001/code_info'
ks_hist_info = '/stock/m002/hist_info'
ks_idx_info = '/stock/m002/code_info'
ks_intra_info = '/stock/m002/intra_info'

kq_code_info = '/stock/m003/code_info'
kq_idx_info = '/stock/m004/code_info'

idx_future_info = '/future/m005/code_info'
stock_future_info = '/future/m091/code_info'

def get_ks_idx_info(id,api) :
    payload = {"cust_id": id, "auth_key": api}
    response = session.post(host_url + ks_idx_info, data=payload)
    if response.status_code == 200:
        json_list = response.json()['results']
        df = pd.DataFrame(columns=['code', 'korname', 'name'])
        for i in json_list:
            code = i[list(json_list[0].keys())[0]]
            korname = i[list(json_list[0].keys())[1]]
            name = i[list(json_list[0].keys())[2]]
            df = df.append({'code': code, 'korname':korname, 'name': name}, ignore_index=True)
    return df

df =  get_ks_idx_info(id,api,ks_idx_info)

def get_kospi_index(id,api, index_name) :
    df_code = get_ks_idx_info(id, api, ks_idx_info)
    jcode = df_code[df_code.korname ==index_name]['code'].tolist()[0]
    payload = {"cust_id": id, "auth_key": api, "jcode" : str(jcode)}
    response = session.post(host_url + ks_hist_info, data=payload)
    json_list = response.json()['results']
    df = pd.DataFrame(columns=['stddate', 'code', 'name', 'prc','prc_diff','rtn','rtn_gb','vol','amt','qty','mktcap','frnrate','fr_mktcap','fr_qty','srt_qty','srt_amt'])
    for i in json_list:
        stddate = i['F12506']
        code = i['F16013']
        name = df_code[df_code.korname ==index_name]['korname'][1]
        prc = i['F15001']
        prc_diff = i['F15472']
        rtn = i['F15004']
        rtn_gb = i['F15006']
        vol = i['F15015']
        amt = i['F15023']
        qty = i['F16143']
        mktcap = i['F15028']
        frnrate = i['F06023']
        fr_mktcap = i['F30812']
        fr_qty = i['F18417']
        srt_qty = i['F33094']
        srt_amt = i['F33095']
        df = df.append({'stddate': stddate, 'code':code, 'name' : name, 'prc': prc, 'prc_diff': prc_diff, 'rtn':rtn, 'rtn_gb': rtn_gb, 'vol': vol, 'amt':amt, 'qty': qty, 'mktcap': mktcap, 'frnrate':frnrate, 'fr_mktcap': fr_mktcap, 'fr_qty': fr_qty, 'srt_qty':srt_qty, 'srt_amt': srt_amt}, ignore_index=True)
    return df
df_idx = get_kospi_index(id,api, "KOSPI 200")

def get_kospi_intra(id,api, index_name) :
    df_code = get_ks_idx_info(id, api, ks_idx_info)
    jcode = df_code[df_code.korname == index_name]['code'].tolist()[0]
    payload = {"cust_id": id, "auth_key": api, "jcode": str(jcode)}
    response = session.post(host_url + ks_intra_info, data=payload)
    json_list = response.json()['results']
    df = pd.DataFrame(columns=['단축코드', '인덱스','체결Intra생성시간', 'Intra시가', 'Intra고가','Intra저가','Intra종가','Intra체결량','Intra거래량','Intra거래대금','Intra누적거래량','Intra누적거래대금','Intra대비','Intra등락률','Intra등락구분'])
    for i in json_list:
        code = i['F16013']
        name = df_code[df_code.korname == index_name]['korname'].tolist()[0]
        datetime = i['F20004_01']
        price_1st = i['F20005_01']
        price_high = i['F20006_01']
        price_low = i['F20007_01']
        price_final = i['F20008_01']
        int_contract = i['F20009_01']
        int_vol = i['F20010_01']
        int_amt = i['F20011_01']
        int_cumvol = i['F20012_01']
        int_cumamt = i['F20013_01']
        prc_diff = i['F20019_01']
        int_rtn = i['F20041_01']
        int_gb = i['F20046_01']
        df = df.append({'단축코드': code, '인덱스':name, '체결Intra생성시간': datetime, 'Intra시가': price_1st, 'Intra고가': price_high, 'Intra저가': price_low, 'Intra종가': price_final,
                        'Intra체결량': int_contract, 'Intra거래량': int_vol, 'Intra거래대금': int_amt, 'Intra누적거래량': int_cumvol, 'Intra누적거래대금' : int_cumamt,
                        'Intra대비': prc_diff, 'Intra등락률': int_rtn, 'Intra등락구분': int_gb}, ignore_index=True)
    return df
df_int = get_kospi_intra(id,api, "소 형 주")


def get_stock_future_info(id,api) :
    payload = {"cust_id": id, "auth_key": api}
    response = session.post(host_url + stock_future_info, data=payload)
    if response.status_code == 200:
        json_list = response.json()['results']
        df = pd.DataFrame(columns=['단축코드','국제표준코드','한글종목명','영문종목명','최근월물구분','만기년월','잔존일수','상장일'])
        for i in json_list:
            code = i[list(json_list[0].keys())[0]]
            engcode = i[list(json_list[0].keys())[1]]
            name = i[list(json_list[0].keys())[2]]
            engname = i[list(json_list[0].keys())[3]]
            gubun = i[list(json_list[0].keys())[4]]
            mat_info = i[list(json_list[0].keys())[5]]
            to_mat = i[list(json_list[0].keys())[6]]
            iss_date = i[list(json_list[0].keys())[7]]
            df = df.append({'단축코드': code, '국제표준코드': engcode, '한글종목명': name, '영문종목명': engname, '최근월물구분': gubun,
                            '만기년월': mat_info, '잔존일수': to_mat, '상장일': iss_date}, ignore_index=True)
    return df
stock_ft_info = get_stock_future_info(id,api)

def get_idx_future_info(id,api) :
    payload = {"cust_id": id, "auth_key": api}
    response = session.post(host_url + idx_future_info, data=payload)
    if response.status_code == 200:
        json_list = response.json()['results']
        df = pd.DataFrame(columns=['단축코드','국제표준코드','한글종목명','영문종목명','최근월물구분','만기년월','잔존일수','상장일'])
        for i in json_list:
            code = i[list(json_list[0].keys())[0]]
            engcode = i[list(json_list[0].keys())[1]]
            name = i[list(json_list[0].keys())[2]]
            engname = i[list(json_list[0].keys())[3]]
            gubun = i[list(json_list[0].keys())[4]]
            mat_info = i[list(json_list[0].keys())[5]]
            to_mat = i[list(json_list[0].keys())[6]]
            iss_date = i[list(json_list[0].keys())[7]]
            df = df.append({'단축코드': code, '국제표준코드': engcode, '한글종목명': name, '영문종목명': engname, '최근월물구분': gubun,
                            '만기년월': mat_info, '잔존일수': to_mat, '상장일': iss_date}, ignore_index=True)
    return df
idx_ft_info = get_stock_future_info(id,api)




