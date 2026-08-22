import requests

def Query_list():

  url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&st=desc&sd=2020-10-16&ed=2021-10-16&qdii=&tabSubtype=,,,,,&pi=1&pn=9999&dx=1"

  payload={}
  headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
    'Accept-Language': 'en,zh;q=0.9,it;q=0.8,zh-CN;q=0.7',
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  response = response.text.replace("var rankData =", "")
  response = response.replace(";", "")
  return response
  

# ln 创建以来
# n 一年, 3n 5n jn, 
# y 1月, 3y 3月, 6y 6月
# ln 创建以来
def _queryScore(Fcode,Dcode):

    url = "https://uni-fundts.1234567.com.cn/dataapi/fund/FundVPageAcc?INDEXCODE=000961&CODE="+Fcode+"&FCODE="+Fcode+"&RANGE="+Dcode+"&CustomerNo=&UserId=&Uid=&CToken=&UToken=&MobileKey=&zone=&DATES=&plat=Iphone&AppType=Iphone&version=6.2.5&Serverversion=6.2.5&appversion=6.2.5"
    payload={}
    headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36',
    'sec-ch-ua-platform': '"Android"',
    'Origin': 'https://h5.1234567.com.cn',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://h5.1234567.com.cn/',
    'Accept-Language': 'en,zh;q=0.9,it;q=0.8,zh-CN;q=0.7'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return(response.text)

def _queryOverview(Fcode):

    url = "https://j5.fund.eastmoney.com/sc/tfs/qt/v2.0.1/"+Fcode+".json?deviceid=123&version=6.3.5&appVersion=6.3.5&product=EFund&plat=Iphone"
    payload={}
    headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Mobile Safari/537.36',
    'sec-ch-ua-platform': '"Android"',
    'Origin': 'https://h5.1234567.com.cn',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://h5.1234567.com.cn/',
    'Accept-Language': 'en,zh;q=0.9,it;q=0.8,zh-CN;q=0.7'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return(response.text)



def queryNet(Fcode,Dcode):

    url = "https://uni-fundts.1234567.com.cn/dataapi/fund/FundNetDiagram2?CODE="+Fcode+"&FCODE="+Fcode+"&RANGE="+Dcode+"&CustomerNo=&UserId=&Uid=&CToken=&UToken=&MobileKey=&zone=&DATES=&POINTCOUNT=&plat=Iphone&AppType=Iphone&product=EFund&version=6.2.5&Serverversion=6.2.5&appversion=6.2.5"
    payload={}
    headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36',
    'sec-ch-ua-platform': '"Android"',
    'Origin': 'https://h5.1234567.com.cn',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://h5.1234567.com.cn/',
    'Accept-Language': 'en,zh;q=0.9,it;q=0.8,zh-CN;q=0.7'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return(response.text)

# @rang : 3y,6y,n
def queryRank(Fcode,Rang):
  
  url = "https://api.fund.eastmoney.com/pinzhong/tlpm?&fundcode="+Fcode+"&range="+Rang

  payload={}
  headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Mobile Safari/537.36',
    'sec-ch-ua-platform': '"Android"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'script',
    'Referer': 'https://fund.eastmoney.com/',
    'Accept-Language': 'en,zh;q=0.9,it;q=0.8,zh-CN;q=0.7'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  return(response.text)
