import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"aue": "lame", "auf": "audio/L16;rate=16000", "vcn": "aisbabyxu", "tte": "utf8"}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}
        #使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        #self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url

class txt_to_voice():
    def __init__(self, sound_file_name = 'answer.mp3'):
        self.APPID = '6035bae5'
        self.APISecret = 'b7e2ffeb156d646bd15ee458651b0494'
        self.APIKey = 'bc8891fd866c6497eb3bacf3d6418478'
        self.sound_file_name = sound_file_name
        self.wsParam = None
        self.ws = None
        self.code = 0
        self.error_message = 'None'
    
    # 收到websocket消息的处理
    def on_message(self, message):
        try:
            message =json.loads(message)
            code = message["code"]
            sid = message["sid"]
            audio = message["data"]["audio"]
            audio = base64.b64decode(audio)
            status = message["data"]["status"]
            self.code = code
            # print(message)
            if status == 2:
                # print("ws is closed")
                # 连接结束
                self.ws.close()
            if code != 0:
                # 收到错误消息
                self.error_message = message["message"]
                # print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            else:
                # 收到音频文件
                with open(self.sound_file_name, 'ab') as f:
                    f.write(audio)

        except Exception as e:
            # 收到内部错误
            self.code = 999
            self.error_message = str(e)
            # print("receive msg,but parse exception:", e)

    # 收到websocket错误的处理
    def on_error(self, error):
        # 网络错误
        self.code = 888
        self.error_message = str(error)

    # 收到websocket关闭的处理
    def on_close(self):
        # print("### closed ###")
        return

    # 收到websocket连接建立的处理
    def on_open(self):
        def run(*args):
            d = {"common": self.wsParam.CommonArgs,
                "business": self.wsParam.BusinessArgs,
                "data": self.wsParam.Data,
                }
            d = json.dumps(d)
            # print("------>开始发送文本数据")
            self.ws.send(d)
            if os.path.exists(self.sound_file_name):
                os.remove(self.sound_file_name)
        # 启动处理线程
        thread.start_new_thread(run, ())

    # 主功能函数
    def convert(self, txt):
        self.wsParam = Ws_Param(APPID=self.APPID, APISecret=self.APISecret, APIKey=self.APIKey, Text=txt)
        websocket.enableTrace(False)
        wsUrl = self.wsParam.create_url()
        self.ws = websocket.WebSocketApp(wsUrl, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return self.code, self.error_message


# Test Demo
if __name__ == "__main__":
    txtToVoice = txt_to_voice()
    code, error_message = txtToVoice.convert("你好呀，我是小书童机器人")
    print("code:{}, error message:{}".format(code, error_message))
