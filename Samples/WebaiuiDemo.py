#-*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import json

URL = "http://openapi.xfyun.cn/v2/aiui"
APPID = "6035bae5"
API_KEY = "1f026dde6738e77a8e555b16c5ae3508"
AUE = "raw"
AUTH_ID = "70e323b8cf9c1a5ce4970e6f14e45ce1"
DATA_TYPE = "text"
SAMPLE_RATE = "16000"
SCENE = "main_box"
RESULT_LEVEL = "complete"
LAT = "39.938838"
LNG = "116.368624"
#个性化参数，需转义
PERS_PARAM = "{\\\"auth_id\\\":\\\"70e323b8cf9c1a5ce4970e6f14e45ce1\\\"}"
FILE_PATH = ""
TEXT = "你好呀"

def buildHeader():
    curTime = str(int(time.time()))
    # param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\"}"
    param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\"}"
    #使用个性化参数时参数格式如下：
    #param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\",\"pers_param\":\""+PERS_PARAM+"\"}"
    param = bytes(param, encoding = "utf8")
    paramBase64 = str(base64.b64encode(param), 'utf-8')

    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + paramBase64).encode("utf8"))
    checkSum = m2.hexdigest()

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
    }
    return header

def readFile(filePath):
    binfile = open(filePath, 'rb')
    data = binfile.read()
    return data

# r = requests.post(URL, headers=buildHeader(), data=readFile(FILE_PATH))
# print(r.content)

r = requests.post(URL, headers=buildHeader(), data=TEXT.encode('utf-8'))
json_r = json.loads(r.content.decode('utf-8'))
code = json_r['code']
print(json_r['data'])
answer = json_r['data'][0]['intent']['answer']['text']
print(answer)
