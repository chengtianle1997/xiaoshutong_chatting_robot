import requests
import time
import hashlib
import base64
import json

class TuringRobot:
    def __init__(self):
        self.URL = "http://openapi.xfyun.cn/v2/aiui"
        self.APPID = "6035bae5"
        self.API_KEY = "1f026dde6738e77a8e555b16c5ae3508"
        self.AUE = "raw"
        self.DATA_TYPE = "text"
        self.SAMPLE_RATE = "16000"
        # 临时场景 main_box, 上线后更改为main
        # self.SCENE = "main"
        self.SCENE = "main_box"
        self.RESULT_LEVEL = "complete"
        # 设备唯一ID身份鉴别，需根据设备生成
        self.AUTH_ID = "70e323b8cf9c1a5ce4970e6f14e45ce1"
        # 地理位置信息，需根据ip或定位获取
        self.LAT = "39.938838"
        self.LNG = "116.368624"
    
    # 请求头建立
    def buildHeader(self):
        curTime = str(int(time.time()))
        # param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\"}"
        param = "{\"result_level\":\""+self.RESULT_LEVEL+"\",\"auth_id\":\""+self.AUTH_ID+"\",\"data_type\":\""+self.DATA_TYPE+"\",\"scene\":\""+self.SCENE+"\",\"lat\":\""+self.LAT+"\",\"lng\":\""+self.LNG+"\"}"
        #使用个性化参数时参数格式如下：
        #param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\",\"pers_param\":\""+PERS_PARAM+"\"}"
        param = bytes(param, encoding = "utf8")
        paramBase64 = str(base64.b64encode(param), 'utf-8')

        m2 = hashlib.md5()
        m2.update((self.API_KEY + curTime + paramBase64).encode("utf8"))
        checkSum = m2.hexdigest()

        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': self.APPID,
            'X-CheckSum': checkSum,
        }
        return header

    # 根据问题获取回答（主功能函数）
    def get_answer(self, txt):
        try:
            r = requests.post(self.URL, headers=self.buildHeader(), data=txt.encode('utf-8'), timeout=5)
            json_r = json.loads(r.content.decode('utf-8'))
            code = int(json_r['code'])
            if code == 0:
                # 获取回答成功，返回代码0及回答内容
                answer = json_r['data'][0]['intent']['answer']['text']
                return code, answer
            else:
                # 图灵接口外部错误，返回错误代码
                return code, "好像哪里出错啦"
        except requests.exceptions.RequestException:
            # 内部错误代码999, 网络超时
            return 999, "网络超时啦，稍等一下再试一次吧"


# Test Demo
if __name__ == "__main__":
    turing_robot = TuringRobot()
    code, answer = turing_robot.get_answer("你好呀")
    print("code: {}, txt: {}".format(code, answer))