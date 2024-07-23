from flask import Flask, request,send_file
from flask_cors import CORS
import json,sys,base64,time
import requests
from vei_api import requestEmotion
import datetime
IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    timer = time.perf_counter

app = Flask(__name__)
CORS(app, resources=r'/*')

API_KEY = '你的百度智能云的API_KEY'
SECRET_KEY = '你的百度智能云的SECRET_KEY'
# 需要识别的文件
AUDIO_FILE = 'output.wav'  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
# 文件格式
FORMAT = 'wav'  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
CUID = '123456PYTHON'
# 采样率
RATE = 16000  # 固定值
# 普通版
DEV_PID = 1537  # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有

# 获取Emotion的Ak和EK
AK = "你的火山引擎账号的AccessKey"
SK = "你的火山引擎账号的SecretKey"

class DemoError(Exception):
    pass

"""  TOKEN start """
# 获取语音转文字的用户token
TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode( 'utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str =  result_str.decode()

    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        #print(SCOPE)
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        #print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')
print(f"token = {fetch_token()}");
"""  TOKEN end """

@app.route('/', methods=['POST'])
def index():
    token = fetch_token()
    if 'file' not in request.files:
        return json.dumps({'error': 'No file found'}), 400
    file = request.files['file']
    if file.filename == "":
        return json.dumps({'error': 'No file selected'}), 400
    filename = None
    if file and file.filename[-3:] == "wav":
        path = './upload/output.wav'
        print(path)
        # file.save(path)
        # return json.dumps("{'filename': filename, 'file_path': file_path}"), 200
    speech_data = file.read()
    print(speech_data)
    length = len(speech_data)
    print("length = " + str(length))
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)
    speech = base64.b64encode(speech_data)
    if (IS_PY3):
        speech = str(speech, 'utf-8')
    params = {'dev_pid': DEV_PID,
             #"lm_id" : LM_ID,    #测试自训练平台开启此项
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    # print post_data
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        print ("Request time cost %f" % (timer() - begin))
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    if (IS_PY3):
        result_str = str(result_str, 'utf-8')
    print(result_str)
    with open("result.txt","w") as of:
        of.write(result_str)

    result = json.loads(result_str)

    # 提取 "result" 字段
    if "result" in result:
        recognition_results = result["result"]
        if recognition_results:  # 确保列表不为空
            # 获取列表中的第一个元素
            speech_text = recognition_results[0]
            print(speech_text)  # 输出
            return json.dumps({'result': speech_text}), 200
        else:
            print("没有识别结果")
    else:
        print("返回结果中没有 'result' 字段")
        return json.dumps({'result': None}), 200
    return json.dumps("抱歉无法连接"),400

#------------------------------------------------------
# 编写传给语音合成的参数
data = {
    "cha_name": "chenlele",
    "text": "",  # 这里应该替换为您实际想要发送的文本
    "save_temp": "True"
}
# ----------------------------------------------------
# 获取语音合成的音频文件
def get_audio():
    url = "http://10.68.133.34:5000/tts"
    # 要发送的数据
    # 发送POST请求
    response = requests.post(url, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        # 设置要保存的文件名
        filename = "speech_output.wav"

        # 保存wav文件
        with open(filename, "wb") as audio_file:
            audio_file.write(response.content)
        print(f"文件已保存为: {filename}")
    else:
        print("API请求失败，状态码：", response.status_code)

# ----------------------------------------------------

@app.route('/heChengAudio', methods = ["POST"])
def heChengAudio():
    text = request.json['text']
    print(text)
    data["text"] = text
    print(data)
    get_audio()
    response = app.make_response(send_file('./speech_output.wav'))
    response.headers['Content-Type'] = 'audio/wav'
    return response, 200

@app.route('/Emotion', methods = ["GET"])
def Emotion():
    now = datetime.datetime.utcnow()
    body = {"device_id": "你要连接的设备编号", "module_identifier": "default"}
    response_body = requestEmotion("POST", now, None, {}, AK, SK, "GetLastDevicePropertyValue", body)
    print(response_body)
    return json.dumps({'Result': response_body["Result"]}), 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)

