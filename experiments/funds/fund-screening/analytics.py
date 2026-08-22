import os
import json
import pandas as pd
from datetime import datetime


def filter_by_manager(file_path):    
    fname = os.path.basename(file_path).split(".")[0].split("-")
    code = fname[0]
    name = fname[1]
    # Opening JSON file to _df
    f = open(file_path)
    obj = json.load(f)
    
    # 基金经理任期未满 1year ，忽略
    data = obj['expansion']['changeInfo']
    columns = ["STYPE", "pdate", "yield"]
    _df = pd.DataFrame(data, columns=columns)
    _df['pdate'] = pd.to_datetime(_df["pdate"], format='%Y-%m-%d')
    _df = _df.set_index("pdate")
    _df_1year = pd.date_range(end = datetime.today().strftime("%Y-%m-%d"), periods=365*1, freq='D')# 创建从今天算起2年的时间序列
    

    
    if _df.index.max() > _df_1year[0]:#如果基金经理, (_df['STYPE'] == "2"??)
    # if _df.index[_df['STYPE'] == "2"].max()>_df_1year[0]: #如果基金经理
        print(name+"基金经理上任不够一年，被忽略")
        return
    

    # 基金侧分
    data = obj['data']
    columns = [
        "pdate",
        "yield",
        "indexYield",
        "fundTypeYield", #同类平均
        "benchQuote"]
    _df = pd.DataFrame(data, columns=columns)
    _df['pdate'] = pd.to_datetime(_df["pdate"], format='%Y-%m-%d')
    _df = _df.set_index("pdate").asfreq('D')

    # 该基金是否有足够测试天数
    _df_2year = pd.date_range(end = datetime.today().strftime("%Y-%m-%d"), periods=365*2, freq='D')# 创建从今天算起2年的时间序列
    if _df.index[0] > _df_2year[0]:
        print(name+"历史太短，被忽略")
        return
    
    # 在测试时间范围内(3year)，该基金是否跑赢'同类平均'次数100%
    _df_3year = pd.date_range(end = datetime.today().strftime("%Y-%m-%d"), periods=365*3, freq='D')# 创建从今天算起3年的时间序列
    _df = _df.reindex(_df_3year).bfill().ffill()# 向前填充，向后填充
    _df["yield"] = _df["yield"].astype(float)
    _df["fundTypeYield"] = _df["fundTypeYield"].astype(float)
    _df['score'] = _df["yield"] - _df["fundTypeYield"]
    num_of_win = (_df['score']>0).sum()
    win_rate = (num_of_win/_df_3year.size)*100
    if win_rate == 100:
        return({
            "code":code,
            "name":name,
            "win_rate":str(win_rate),
            "win_score":str(_df['score'].sum())
        })
        

