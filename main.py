import json
import re
import os
import glob
import pandas as pd
from pathlib import Path
from datetime import datetime
from query_data import Query_list,_queryOverview,queryNet,queryRank
from analytics import filter_by_manager

# [Dwonload] For request funds data, first to get All funds name and code 
print("[Dwonload] list of all funds")
response = Query_list() # get a new 'list_of_all_funds.csv'
data = re.sub("(\w+):", r'"\1":',  response)
data = json.loads(data)
# Write csv files 
PATH_ALL_FUNDS = "report/list_of_all_funds.csv"
CSVheaders = "代码,基金,基金简称,日期,单位净值,累计净值,日增长率,近1周,近1月,近3月,近6月,近1年,近2年,近3年,今年来,成立来,成立日,,,,,,手续费,,"
with open(PATH_ALL_FUNDS, 'w+', encoding='UTF8', newline='') as f:
    f.write(CSVheaders+'\n')
    for row in data["datas"]:
        f.write(row+'\n')


df = pd.read_csv(PATH_ALL_FUNDS) # "fund_list.csv"
df['代码'] = df['代码'].apply(str).apply(lambda x: x.zfill(6))
# [FILTER] 近6月,近1年,近2年,近3年 收益必须都为正
df = df.loc[(df['近1年'] >= 15)&(df['近2年'] >= 30) & (df['近3年'] >= 45)]
# df = df.loc[(df['近6月'] >= 7)&(df['近1年'] >= 15)&(df['近2年'] >= 30) & (df['近3年'] >= 45)]
print("[FILTER] 近6月,近1年,近2年,近3年 收益达预期, 过滤后：%d" %len(df.index))
# [Dwonload] Overview
PATH_OVERVIEW_FOLDER = "report/overview/"
for index, row in df.iterrows():
    Fcode = row["代码"]
    name = row["基金"].replace("/", "")
    filesName =  Fcode+ "-"+ name+ '.json'
    Path(PATH_OVERVIEW_FOLDER).mkdir(parents=True, exist_ok=True)
    # If downloaded?
    if not os.path.isfile(PATH_OVERVIEW_FOLDER+filesName):
        response = _queryOverview(Fcode)
        with open(PATH_OVERVIEW_FOLDER+filesName, 'w+', encoding='UTF8') as f:
            f.write(response) 





# [FILTER] Overview
path_all_json_overviews = glob.glob("report/overview/*.json")
output = []
for path in path_all_json_overviews:
    f = open (path, "r")
    res = json.loads(f.read())
    Name = res["JJXQ"]["Datas"]["SHORTNAME"]
    Fcode = res["JJXQ"]["Datas"]["FCODE"]
    
    # 资金规模 < 200000000
    if res["JJXQ"]["Datas"]["ENDNAV"]!='--' and float(res["JJXQ"]["Datas"]["ENDNAV"]) < 200000000.0:
        print("%s-%s 资金规模 < 2亿"%(Fcode,Name))
        continue


    # 基金经理任期经历一次牛熊（2015）
    managers_data = res["JJJL"]["Expansion"]
    _df_m = pd.DataFrame(managers_data)
    _df_m["DAYS"] = pd.to_numeric(_df_m["DAYS"], downcast="float")
    selected_nanager_data = _df_m.loc[_df_m['DAYS'].idxmax()]
    count_of_manager = len(managers_data)
    if count_of_manager>1:
        print("%s-%s %d个基金经理管理"%(Fcode,Name,count_of_manager))

        # manger_on_market_year = 
        
    manger_on_market_year = float(selected_nanager_data["TOTALDAYS"])
    duration = datetime.now()  - datetime(2014, 10, 24)
    duration =  divmod(duration.total_seconds(), 86400)[0] 
    if manger_on_market_year - duration < 0.0:
        print("%s-%s Manager从业时间未能经历一次牛熊（2015）"%(Fcode,Name))
        continue

    # 基金经理管理时间内
    manger_operate_year = float(selected_nanager_data["DAYS"])/365.0
    max_rop5 =  res["TSSJ"]["Datas"]["MAXRETRA5"]
    max_rop3 =  res["TSSJ"]["Datas"]["MAXRETRA3"]
    max_rop1 =  res["TSSJ"]["Datas"]["MAXRETRA1"]
    if manger_operate_year < 1: #少于1年忽略
        print("%s-%s Manager管理时间少于1年"%(Fcode,Name))
        continue
        # 基金经理最大回撤 < 35% 
    elif manger_operate_year >= 5.0 and max_rop5!='--' and float(max_rop5) > 35.0:
        print("%s-%s Manager MDD > 35percent, in 5 y"%(Fcode,Name))
        continue
    elif manger_operate_year >= 3.0 and res["TSSJ"]["Datas"]["MAXRETRA3"]!='--' and float(res["TSSJ"]["Datas"]["MAXRETRA3"])> 35.0:
        print("%s-%s Manager MDD > 35percent, in 3 y"%(Fcode,Name))
        continue
    elif manger_operate_year >= 1.0 and float(res["TSSJ"]["Datas"]["MAXRETRA1"])> 35.0:
        print("%s-%s Manager MDD > 35percent, in 1 y"%(Fcode,Name))
        continue    
    
    

    # write report 
    report ={
        "NAME":Name,
        "CODE":Fcode,
        "FTYPE":res["JJXQ"]["Datas"]["FTYPE"],
        "BFUNDTYPE":res["JJXQ"]["Datas"]["BFUNDTYPE"],
        "FUNDTYPE":res["JJXQ"]["Datas"]["FUNDTYPE"],
        "SHARP1":res["JJXQ"]["Datas"]["SHARP1"]if manger_operate_year>=1.0 else None,
        "SHARP2":res["JJXQ"]["Datas"]["SHARP2"]if manger_operate_year>=2.0 else None,
        "SHARP3":res["JJXQ"]["Datas"]["SHARP3"]if manger_operate_year>=3.0 else None,
        "MAXRETRA1":res["TSSJ"]["Datas"]["MAXRETRA1"]if manger_operate_year>=1.0 else None,
        "MAXRETRA3":res["TSSJ"]["Datas"]["MAXRETRA3"]if manger_operate_year>=3.0 else None,
        "MAXRETRA5":res["TSSJ"]["Datas"]["MAXRETRA5"]if manger_operate_year>=5.0 else None,
        "MGRID":selected_nanager_data["MGRID"],
        "MGRNAME":selected_nanager_data["MGRNAME"],
        "HJ_JN":selected_nanager_data["HJ_JN"],
        "TOTALDAYS":selected_nanager_data["TOTALDAYS"],
        "DAYS":selected_nanager_data["DAYS"],
        # "RANK":rank,
    }

    output.append(report)

df2 = pd.DataFrame(output)
PATH_OVERVIEW_CSV = "report/overview_filtered_manager.csv"
df2.to_csv(PATH_OVERVIEW_CSV)




# RanK [3Y,6Y,N]
# # 管理期内一年同类 Rank 
RANK_RANGES = ["1n","6y","3y"]# "3y",
PATH_RANK_CSV= "report/rank.csv"

df2 = pd.read_csv(PATH_OVERVIEW_CSV)
df2['CODE'] = df2['CODE'].apply(str).apply(lambda x: x.zfill(6))
for rang in RANK_RANGES:

    path_rank_folder = "report/rank/"+rang+"/"
    for index, row in df2.iterrows():
        filesName = row["CODE"] + "-" + row["NAME"].replace("/", "")
        Path(path_rank_folder).mkdir(parents=True, exist_ok=True)
        # If downloaded?
        if not os.path.isfile(path_rank_folder+filesName+".json"):
            response  = queryRank(row["CODE"],rang)
            with open(path_rank_folder+filesName+".json", 'w+', encoding='UTF8') as f:
                f.write(response) 

    # analytic
    rank_paths = glob.glob(path_rank_folder+"*.json")
    key_of_rank = 'RANK'+ rang.upper()
    for path in rank_paths:
        fname = os.path.basename(path).split(".")[0].split("-")
        code = fname[0]
        name = fname[1]
        f = open (path, "r")
        res = json.loads(f.read())
        _df = pd.DataFrame(res["Data"]) 
        _df['x'] = _df['x'].mul(1e6).apply(pd.Timestamp)
        _df = _df.loc[(_df["sc"] != '--')] #could not convert string to float: '--' _df["sc"] = _df["sc"].astype(float) 
        _df["sc"] = _df["sc"].astype(float)
        # _df["x"] = pd.to_datetime(_df["x"], format='%Y-%m-%d')
        # 管理期内
        # 有时候rank 提供的数据未达到经理的管理时间
        _df = _df.set_index("x") # 不填充，将来将NaN的数据（关闭日）排除
        _df.index = _df.index.floor('D') # 去掉小时
        _rank_days = (datetime.today() - _df.index[0]).days
        _daysOverview = int(df2.loc[(df2["CODE"]==code),"DAYS"])
        _rank_days = _daysOverview if _daysOverview < _rank_days else _rank_days
        _operate_periodo = pd.date_range(end = datetime.today().strftime("%Y-%m-%d"), periods=_rank_days, freq='D')# 创建从今天算起3年的时间序列
        
        _df = _df.reindex(_operate_periodo)
        rank_mean =  (_df["y"] / _df["sc"]).mean()
        # if rank_mean > 0.5 :
        #     continue
        df2.loc[(df2["CODE"]==code), key_of_rank] = rank_mean
    df2 = df2.loc[(df2[key_of_rank] <0.333)] #将过滤（刷新）df2 内不符合标准的基金，也不会进行下一轮 query

df2["RANK"] = df2["RANK1N"]+df2["RANK6Y"]+df2["RANK3Y"]
df2.to_csv(PATH_RANK_CSV)









# PATH_OVERVIEW_FOLDER = "report/overview/"
# for index, row in df.iterrows():
#     Fcode = row["代码"]
#     name = row["基金"].replace("/", "")
#     filesName =  Fcode+ "-"+ name+ '.json'
#     Path(PATH_OVERVIEW_FOLDER).mkdir(parents=True, exist_ok=True)
#     # If downloaded?
#     if not os.path.isfile(PATH_OVERVIEW_FOLDER+filesName):
#         response = _queryOverview(Fcode)
#         with open(PATH_OVERVIEW_FOLDER+filesName, 'w+', encoding='UTF8') as f:
#             f.write(response) 



#     data = res["JDZF"]["Datas"]
#     _df = pd.DataFrame(data, columns=["title","rank","sc"])
#     _df["rank"] = pd.to_numeric(_df["rank"], downcast="float")
#     _df["sc"] = pd.to_numeric(_df["sc"], downcast="float")
#     _df = _df.loc[( _df["rank"] < _df["sc"]/2)] # 筛选出优于同类的排名数据
#     pass_periodo = ["Y","3Y","6Y","1N","JN"]
#     if manger_operate_year >= 5.0:
#         pass_periodo = pass_periodo +["2N","3N","5N"]  
#     elif manger_operate_year >= 3.0:
#         pass_periodo = pass_periodo +["2N","3N"] 
#     elif manger_operate_year >= 2.0:
#         pass_periodo = pass_periodo +["2N"]
#     if not set(pass_periodo).issubset(_df["title"].unique()): # 如果时间代码不在了，说明没有通过
#         print("%s-%s rank 不能长期跑赢同类"%(Fcode,Name)) # "Z","3N""Y","3Y",
#         continue
    
#     rank = (_df["rank"]/_df["sc"]).mean()

# # NET.json ()
# PATH_OVERVIEW_CSV = "report/overview_filtered.csv"
# PATH_NET_FOLDER = "report/NET/"
# Path(PATH_NET_FOLDER).mkdir(parents=True, exist_ok=True)
# df = pd.read_csv(PATH_OVERVIEW_CSV) # "fund_list.csv"
# df["CODE"] = df["CODE"].apply(str).apply(lambda x: x.zfill(6))

# Dcode = "ln"
# for index, row in df.iterrows():
#     filesName =  row["CODE"] + "-"+ row["NAME"]+ '.json'
#     # check if downloaded?
#     if not os.path.isfile(PATH_NET_FOLDER+filesName):
#         response = queryNet(row["CODE"],Dcode)
#         with open(PATH_NET_FOLDER+filesName, 'w+', encoding='UTF8') as f:
#             f.write(response) 
    

















# According list, query fund's json about `SCORE,Manager` with Duration `ln`
# # Score json ()
#     Dcode = "ln"
#     floderPath = "report/score/"+ Dcode + "/"
#     filesName =  Fcode+ "-"+ name+ '.json'
#     Path(floderPath).mkdir(parents=True, exist_ok=True)
#     # check if downloaded?
#     if not os.path.isfile(floderPath+filesName):
#         data = _queryScore(Fcode,Dcode)
#         with open(floderPath+filesName, 'w+', encoding='UTF8') as f:
#             f.write(data)

# # 1st Analytic , filter by Manager and funds history.
# print("1st Analytic , filter by Manager and funds history.")
# funds_path = glob.glob("report/score/ln/*.json")
# output = []
# for path in funds_path:
#     res = filter_by_manager(path)
#     if res is not None:
#         output.append(res)

# df = pd.DataFrame(data = output ,columns=["code","name","win_score","win_rate"])
# df.to_csv("report/filtered_01.csv")

# # 2nd Analytic, 
# print("2nd Analytic")





