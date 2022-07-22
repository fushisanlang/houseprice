import requests
import json
from readconf import ReadConf

def PriceLog(logStr):
    #print(logStr)
    return

def SendMessage(MessageStr):
    url = ReadConf("Qywx", "Url")
    MessageJson = {"msgtype": "text", "text": {"content": MessageStr}}
    MessageJsonDumps = json.dumps(MessageJson)
    requests.post(url, MessageJsonDumps, headers={
                  'Content-Type': 'application/json;charset=utf-8'})
    return

