# built from xunfei demo
# to generate from pinyin:
# http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=15340

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

from jiezi.settings import MEDIA_ROOT


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
        self.BusinessArgs = {"aue": "lame",
                             "auf": "audio/L16;rate=16000",
                             "vcn": "aisxping",
                             "speed": 10,
                             "tte": "utf8"}
        self.Data = {"status": 2, "text": str(base64.b64encode(
            self.Text.encode('utf-8')), "UTF8")}
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


def get_text_audio(text, filepath):
    def on_message(ws, message):
        try:
            message = json.loads(message)
            code = message["code"]
            sid = message["sid"]
            audio = message["data"]["audio"]
            audio = base64.b64decode(audio)
            status = message["data"]["status"]
            print(message)
            if status == 2:
                print("ws is closed")
                ws.close()
            if code != 0:
                errMsg = message["message"]
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            else:
                with open(filepath, 'ab') as f:
                    f.write(audio)

        except Exception as e:
            print("receive msg,but parse exception:", e)

    # 收到websocket错误的处理
    def on_error(ws, error):
        print("### error:", error)


    # 收到websocket关闭的处理
    def on_close(ws):
        print("### closed ###")


    # 收到websocket连接建立的处理
    def on_open(ws):
        def run(*args):
            d = {"common": wsParam.CommonArgs,
                 "business": wsParam.BusinessArgs,
                 "data": wsParam.Data,
                 }
            d = json.dumps(d)
            print("------>开始发送文本数据")
            ws.send(d)
            if os.path.exists(filepath):
                os.remove(filepath)

        thread.start_new_thread(run, ())

    wsParam = Ws_Param(APPID='5f6db427',
                       APIKey='0c25f66a177451f5a34c25967f0fad0f',
                       APISecret='66b1414b20e556084d8f10ce2af2fc48',
                       Text=text)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE},
                   ping_interval=2, ping_timeout=1)


def get_audio(pinyin=None, chinese=None):
    dir_path = os.path.join(MEDIA_ROOT, 'audio/')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if pinyin:
        if '/' in pinyin:
            pinyins = pinyin.split('/')
            query = ""
            for i, pinyin in enumerate(pinyins):
                query += f'拼[={pinyin.strip()}]'
                if i != len(pinyins) - 1:
                    query += '[p500]'
        else:
            query = f"拼[={pinyin}]"
    elif chinese:
        query = chinese
    else:
        raise Exception("Either pinyin or chinese must be specified")
    filename = f"{query}.mp3"

    path = os.path.join(dir_path, filename)
    if not os.path.exists(path):
        get_text_audio(query, path)

    return f'/media/audio/{filename}'


def generate_audio_tag(pinyin=None, chinese=None):
    path = get_audio(pinyin=pinyin, chinese=chinese)
    return f"""
    <audio id="audio">
      <source src="{path}" type="audio/mpeg">
      You browser doesn't support audio
    </audio>
    <i class='fas fa-volume' style='cursor: pointer;'
      onclick='document.getElementById("audio").play()'></i>
    """



if __name__ == '__main__':
    query = "你"
    get_text_audio(query, f'../media/{query}.mp3')