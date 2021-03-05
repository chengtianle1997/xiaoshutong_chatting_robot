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

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

# -------------- 错误信息 ------------------ #
# code :888   websocket错误（网络连接错误）
# code :999   消息内部错误

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, AudioFile):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo":1,"vad_eos":10000}

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
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

class voice_to_txt():
    def __init__(self, sound_file_name='question.mp3'):
        self.APPID = '6035bae5'
        self.APISecret = 'b7e2ffeb156d646bd15ee458651b0494'
        self.APIKey = 'bc8891fd866c6497eb3bacf3d6418478'
        self.sound_file_name = sound_file_name
        self.wsParam = None
        self.ws = None
        self.encoding = 'lame'
        self.code = 0
        self.txt = ''
        self.error_message = 'None'
    
    # 收到websocket消息的处理
    def on_message(self, ws, message):
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            self.code = code
            if code != 0:
                # 收到外部错误代码
                errMsg = json.loads(message)["message"]
                # print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
                self.error_message = errMsg
            else:
                data = json.loads(message)["data"]["result"]["ws"]
                # print(json.loads(message))
                result = ""
                for i in data:
                    for w in i["cw"]:
                        result += w["w"]
                # print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))
                # print(result)
                self.txt += result
                # if json.loads(message)["data"]["result"]["ls"] == True:
                #     print("识别结果:%s" % (self.txt))
                #     text = ''
        except Exception as e:
            # print("receive msg,but parse exception:", e)
            # 内部消息错误 999
            self.code = 999
            self.error_message = str(e)

    # 收到websocket错误的处理
    def on_error(self, ws, error):
        # print("### error:", error)
        self.code = 888
        self.error_message = str(error) 

    # 收到websocket关闭的处理
    def on_close(self, ws):
        # print("### closed ###")
        return

    # 收到websocket连接建立的处理
    def on_open(self, ws):
        def run(*args):
            frameSize = 8000  # 每一帧的音频大小
            intervel = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

            with open(self.wsParam.AudioFile, "rb") as fp:
                while True:
                    buf = fp.read(frameSize)
                    # 文件结束
                    if not buf:
                        status = STATUS_LAST_FRAME
                    # 第一帧处理
                    # 发送第一帧音频，带business 参数
                    # appid 必须带上，只需第一帧发送
                    if status == STATUS_FIRST_FRAME:

                        d = {"common": self.wsParam.CommonArgs,
                            "business": self.wsParam.BusinessArgs,
                            "data": {"status": 0, "format": "audio/L16;rate=16000",
                                    "audio": str(base64.b64encode(buf), 'utf-8'),
                                    "encoding": self.encoding}}
                        d = json.dumps(d)
                        self.ws.send(d)
                        status = STATUS_CONTINUE_FRAME
                    # 中间帧处理
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                    "audio": str(base64.b64encode(buf), 'utf-8'),
                                    "encoding": self.encoding}}
                        self.ws.send(json.dumps(d))
                    # 最后一帧处理
                    elif status == STATUS_LAST_FRAME:
                        d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                    "audio": str(base64.b64encode(buf), 'utf-8'),
                                    "encoding": self.encoding}}
                        self.ws.send(json.dumps(d))
                        time.sleep(1)
                        break
                    # 模拟音频采样间隔
                    time.sleep(intervel)
            self.ws.close()
        # 启动处理线程
        thread.start_new_thread(run, ())

    # 主功能函数
    def convert(self, sound_file_name=None):
        if not sound_file_name == None:
            self.sound_file_name = sound_file_name
        self.txt = ''
        self.code = 0
        self.error_message = 'None'
        self.wsParam = Ws_Param(APPID=self.APPID, APISecret=self.APISecret,
                       APIKey=self.APIKey,
                       AudioFile=self.sound_file_name)
        websocket.enableTrace(False)
        wsUrl = self.wsParam.create_url()
        self.ws = websocket.WebSocketApp(wsUrl, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return self.code, self.txt, self.error_message

# Test Demo
if __name__ == '__main__':
    VoiceToTxt = voice_to_txt()
    code, txt, error_message = VoiceToTxt.convert()    
    print("code: {}, txt: {}, error message: {}".format(code, txt, error_message))
