import requests
import sys
from dboperaction import InsertOperaction
from pricetools import PriceLog

# 准备步骤，建立城市列表
CityList = [{"CityName": "长春", "CityAbbreviation": "cc"}]
# 第一步：根据城市简写获取一级分类列表
# 输入城市简写
def getDistrictNameList(CityList):
    CityAbbreviation = CityList['CityAbbreviation']
    CityName = CityList['CityName']
    url = 'https://fangjia.fang.com/fangjia/map/getmapdata/' + CityAbbreviation
    try:
        data = requests.get(url)
        DistrictDataList = data.json()['project']
    except:
        PriceLog("获取信息失败，正在退出")
        sys.exit(1)
    else:
        DistrictList = []
        DistrictDict = {}
        for DistrictData in DistrictDataList:
            DistrictDict['CityName'] = CityName
            DistrictDict["CityAbbreviation"] = CityAbbreviation
            DistrictDict["DistricName"] = DistrictData["name"]
            DistrictList.append(DistrictDict.copy())
        return DistrictList
'''
[
    {   
        "CityName":"",
        "CityAbbreviation":"",
        "DistricName":""
    },
    ...........
]
'''

# 第二步，根据一级分类列表循环获取二级分类
'''
{
    "CityName":"",
    "CityAbbreviation":"",
    "DistricName":""
}
输入的是dict，输出是dict的list
'''
def getStreetNameList(DistrictDict):
    CityName = DistrictDict['CityName']
    CityAbbreviation = DistrictDict["CityAbbreviation"]
    DistrictName = DistrictDict["DistricName"]
    url = "https://fangjia.fang.com/fangjia/map/getmapdata/" + CityAbbreviation + "?district=" + \
        DistrictName + "&commerce=&x1=undefined&y1=undefined&x2=undefined&y2=undefined&v=20150116&newcode="
    StreetDict = {}
    StreetNameList = []
    try:
        data = requests.get(url)
        StreetDataList = data.json()['project']
    except:
        PriceLog("获取信息失败，正在退出")
        sys.exit(1)
    else:
        for StreetData in StreetDataList:
            StreetDict["CityName"] = CityName
            StreetDict["CityAbbreviation"] = CityAbbreviation
            StreetDict["DistrictName"] = DistrictName

            StreetDict["StreetName"] = StreetData['name']
            StreetNameList.append(StreetDict.copy())
    return StreetNameList
'''
[
    {
        "CityName":"",
        "CityAbbreviation":"",
        "DistricName":"",
        "StreetName":""
    },
    ...........
]
'''

# 第三步，根据街道信息获取小区名称和id
'''
{
    "CityName":"",
    "CityAbbreviation":"",
    "DistricName":"",
    "StreetName":""
}
'''
def getCommunityNameIDList(StreetDict):
    CityName = StreetDict["CityName"]
    CityAbbreviation = StreetDict["CityAbbreviation"]
    DistrictName = StreetDict["DistrictName"]
    StreetName = StreetDict["StreetName"]
    url = 'https://fangjia.fang.com/fangjia/map/getmapdata/' + \
        CityAbbreviation + '?district=' + DistrictName + '&commerce=' + StreetName
    CommunityInfoDict = {}
    CommunityNameIDList = []
    try:
        data = requests.get(url)
        CommunityDatas = data.json()["project"]
    except:
        PriceLog("获取信息失败，正在退出")
        sys.exit(1)
    else:
        for CommunityData in CommunityDatas:
            CommunityInfoDict["CityName"] = CityName
            CommunityInfoDict["CityAbbreviation"] = CityAbbreviation
            CommunityInfoDict["DistrictName"] = DistrictName
            CommunityInfoDict["StreetName"] = StreetName
            CommunityInfoDict["CommunityName"] = CommunityData['name']
            CommunityInfoDict["CommunityId"] = CommunityData['url'].split(
                '/', -1)[-1].split('.', -1)[0]
            CommunityNameIDList.append(CommunityInfoDict.copy())
    print(CommunityNameIDList)
    return CommunityNameIDList

'''
[
    {
        "CityName":"",
        "CityAbbreviation":"",
        "DistricName":"",
        "StreetName":"",
        "CommunityName":"",
        "CommunityId":""
    },
    ...........
]
'''

# 第四步，获取小区房价
def getCommunityPriceList(CommunityInfoDict):
    CityName = CommunityInfoDict["CityName"]
    CityAbbreviation = CommunityInfoDict["CityAbbreviation"]
    DistrictName = CommunityInfoDict["DistrictName"]
    StreetName = CommunityInfoDict["StreetName"]
    CommunityName = CommunityInfoDict["CommunityName"]
    CommunityId = CommunityInfoDict["CommunityId"]
    url = 'https://fangjia.fang.com/fangjia/common/ajaxdetailtrenddata/' + \
        CityAbbreviation + '?dataType=proj&projcode=' + \
        str(CommunityId) + '&year=2'
    CommunityPriceDict = {}
    CommunityPriceList = []
    try:

        data = requests.get(url)
        CommunityPrices = data.json()
    except:
        PriceLog("获取信息失败，正在退出")
        sys.exit(1)
    else:
        for CommunityPrice in CommunityPrices:
            CommunityPriceDict["CityName"] = CityName

            CommunityPriceDict["CityAbbreviation"] = CityAbbreviation
            CommunityPriceDict["DistrictName"] = DistrictName
            CommunityPriceDict["StreetName"] = StreetName
            CommunityPriceDict["CommunityName"] = CommunityName
            CommunityPriceDict["CommunityId"] = CommunityId
            CommunityPriceDict["timestampstr"] = CommunityPrice[0]
            CommunityPriceDict["price"] = CommunityPrice[1]
            CommunityPriceList.append(CommunityPriceDict.copy())
    return CommunityPriceList

#第五步 组装sql
def saveCommunityPrice(CommunityPriceDict):
    CityName = CommunityPriceDict["CityName"]
    CityAbbreviation = CommunityPriceDict["CityAbbreviation"]
    DistrictName = CommunityPriceDict["DistrictName"]
    StreetName = CommunityPriceDict["StreetName"]
    CommunityName = CommunityPriceDict["CommunityName"]
    CommunityId = CommunityPriceDict["CommunityId"]
    timestampstr = CommunityPriceDict["timestampstr"]
    price = CommunityPriceDict["price"]
    sql = "INSERT INTO communitydata (cityname, cityabbreviation, districtname, streetname, communityname, communityid, timestampstr, price) VALUES ('" + CityName + "', '" + CityAbbreviation + "', '" + DistrictName + "', '" + StreetName  + "', '" + CommunityName  + "', " +  str(CommunityId )  + ", " + str(timestampstr) + ", " +  str(price) + ");"
    InsertOperaction(sql)
    return 


for City in CityList:
    DistrictNameList = getDistrictNameList(City)
    for DistrictName in DistrictNameList:
        StreetNameList = getStreetNameList(DistrictName)
        for StreetName in StreetNameList:
            CommunityNameIDList = getCommunityNameIDList(StreetName)
            for CommunityNameID in CommunityNameIDList:
                CommunityPriceList = getCommunityPriceList(CommunityNameID)
                for CommunityPrice in CommunityPriceList:
                    saveCommunityPrice(CommunityPrice)
                break
            break
        break
    break
