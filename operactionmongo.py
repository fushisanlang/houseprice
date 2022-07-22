#!/usr/bin/python3
import pymongo
from readconf import ReadConf
import time
from pricetools import SendMessage,PriceLog


def InsertOperaction(DataDict):
    '''
    {
        "DataDB":"houseprice",
        "DataCollection":"cc_communityprice",
        "DataJson"={'CityName': '长春', 'CityAbbreviation': 'cc', 'DistrictName': '宽城', 'StreetName': '光复路', 'CommunityName': '光复路小区', 'CommunityId': '1710783703', 'CommunityPrice': [[1593532800000, 7803], [1596211200000, 8623], [1598889600000, 8607], [1601481600000, 8204], [1604160000000, 7646], [1606752000000, 6984], [1612108800000, 8379], [1614528000000, 7441], [1617206400000, 7552], [1619798400000, 7871], [1622476800000, 7865], [1625068800000, 7544], [1627747200000, 7343], [1630425600000, 7459], [1633017600000, 7638], [1635696000000, 7412], [1638288000000, 7245], [1640966400000, 7272], [1643644800000, 7251], [1646064000000, 7542], [1648742400000, 7587], [1651334400000, 7535], [1654012800000, 7438], [1656604800000, 7273]]}
    }
    '''
    DataJson=DataDict["DataJson"]
    DataDB = DataDict["DataDB"]
    DataCollection= DataDict["DataCollection"]
    MongoUrl = ReadConf("MongoServer", "CientUrl")
    myclient = pymongo.MongoClient(MongoUrl)
    mydb = myclient[DataDB]
    mycol = mydb[DataCollection]

    try:
        mycol.insert_one(DataJson)
    except:
        PriceLog("存储信息失败，正在退出")
        PriceLog(DataDict)
        time.sleep(1)
    return