import asyncio
import os
# import aiohttp
from pathlib import Path




async def _get_request(session, url, fcode):
    async with session.get(url) as resp:
        response = await resp.text()
        return {"data": response, "code": str(fcode)}


async def aio_queryOverview(codes, output_folder):
    ext = ".json"
    head = {
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
    async with aiohttp.ClientSession(headers=head) as session:
        tasks = []
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        for Fcode in codes:
            filesName = str(Fcode) + ext
            # If downloaded?
            if not os.path.isfile(output_folder + filesName):
                url = "https://j5.fund.eastmoney.com/sc/tfs/qt/v2.0.1/" + \
                    str(Fcode)+".json?deviceid=123&version=6.3.5&appVersion=6.3.5&product=EFund&plat=Iphone"
                tasks.append(asyncio.ensure_future(
                    _get_request(session, url, Fcode)))

        
        responses = await asyncio.gather(*tasks)
        for res in responses:
            with open(output_folder + res["code"] + ext, 'w+', encoding='UTF8') as f:
                f.write(res["data"])
# PATH_OVERVIEW_FOLDER = "test/"
# Fcodes = [980003,970071,970069,970067,970057,970056,970048,970045,970043,970042,970038,970035,970033,970031,970030,970027,970026,970022,970021,970019,970017,970016,970015,970014,970013,970012,970010,970008,970007,970005,970004,959991,952320,952313,952099,952035,952024,952020,952013,952004,920928,920927,920923,920922,920921,920011,920008,920007,920003,920002,900152,900133,900112,900100,900099,900097,900090,900089,900087,900079,900078,900077,900059,900052,900039,900030,900029,900019,900015,900013,900012,900009,900008,900007,900003,881011,881010,880007,872021,872019,872017,872016,872015,872014,871003,870017,870009,870008,870005,865040,862012,862001,860063,860058,860056,860055,860053,860052,860051,860050,860039,860038,860037,860036,860035,860033,860030,860029,860028,860022,860012,860009,860005,855001,851880,851860,851836,851830,850699,850688,850599,850588,850099,850088,850003,770001,762001,750005,750003,750002,750001,740101,740001,730002,730001,720003,720002,720001,710302,710301,710002,710001,700006,700005,700004,700003,700002,700001,690202,690012,690011,690009,690008,690007,690005,690004,690003,690002,690001,688888,686869,686868,675163,675161,675123,675121,675113,675111,675100,675093,675091,675083,675081,675053,675051,675043,675041,675013,675011,673143]
# asyncio.run(aio_queryOverview(codes= Fcodes, output_folder=PATH_OVERVIEW_FOLDER))


async def aio_queryRank(codes, Rang, output_folder):
    ext=".json"
    head = {
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
    async with aiohttp.ClientSession(headers=head) as session:
        
        path_rank_folder = output_folder 
        tasks = []
        for Fcode in codes:
            filesName = str(Fcode) + ext
            # If downloaded?
            if not os.path.isfile(path_rank_folder + filesName):
                url = "https://api.fund.eastmoney.com/pinzhong/tlpm?&fundcode=" + \
                    str(Fcode)+"&range="+Rang
                tasks.append(asyncio.ensure_future(
                    _get_request(session, url, Fcode)))

        responses = await asyncio.gather(*tasks)
        Path(path_rank_folder).mkdir(parents=True, exist_ok=True)
        for res in responses:
            with open(path_rank_folder + res["code"] + ext, 'w+', encoding='UTF8') as f:
                f.write(res["data"])
# PATH_OVERVIEW_FOLDER = "test/"
# Fcodes = [980003, 970071, 970069, 970067, 970057, 970056, 970048, 970045, 970043, 970042, 970038, 970035, 970033, 970031, 970030, 970027, 970026, 970022, 970021, 970019, 970017, 970016, 970015, 970014, 970013, 970012, 970010, 970008, 970007, 970005, 970004, 959991, 952320, 952313, 952099, 952035, 952024, 952020, 952013, 952004, 920928, 920927, 920923, 920922, 920921, 920011, 920008, 920007, 920003, 920002, 900152, 900133, 900112, 900100, 900099, 900097, 900090, 900089, 900087, 900079, 900078, 900077, 900059, 900052, 900039, 900030, 900029, 900019, 900015, 900013, 900012, 900009, 900008, 900007, 900003, 881011, 881010, 880007, 872021, 872019, 872017, 872016, 872015, 872014, 871003, 870017, 870009, 870008, 870005,
#           865040, 862012, 862001, 860063, 860058, 860056, 860055, 860053, 860052, 860051, 860050, 860039, 860038, 860037, 860036, 860035, 860033, 860030, 860029, 860028, 860022, 860012, 860009, 860005, 855001, 851880, 851860, 851836, 851830, 850699, 850688, 850599, 850588, 850099, 850088, 850003, 770001, 762001, 750005, 750003, 750002, 750001, 740101, 740001, 730002, 730001, 720003, 720002, 720001, 710302, 710301, 710002, 710001, 700006, 700005, 700004, 700003, 700002, 700001, 690202, 690012, 690011, 690009, 690008, 690007, 690005, 690004, 690003, 690002, 690001, 688888, 686869, 686868, 675163, 675161, 675123, 675121, 675113, 675111, 675100, 675093, 675091, 675083, 675081, 675053, 675051, 675043, 675041, 675013, 675011, 673143]
# asyncio.run(aio_queryRank(codes=Fcodes, output_folder=PATH_OVERVIEW_FOLDER,Rang="3Y"))
