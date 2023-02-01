print("start!")
import ChatWaifuServer
import librosa
import requests
import json
from hashlib import md5
import random
import socket
from pydub import AudioSegment
print("import finish!")

appid = '20230201001546983'
appkey = 'VpIt2YAdqu99rhz1hP6e'
# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'auto'
to_lang =  'jp'
endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

ip_port = ('127.0.0.1', 9000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
s.bind(ip_port)
s.listen(5)
while True:
    connection, address = s.accept()
    connection.settimeout(15)  # 5s
    print("************连接成功*************")
    connection.send(str("success").encode())
    data = connection.recv(1024)
    data = data.decode()

    query = data
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    print(result)
    trans = result['trans_result'][0]['dst']
    print(trans)
    print("************开始生成*************")
    model_path = "model/365_epochs.pth"
    config_path = "model/config.json"
    # 文本/模型内部序号/中英文/模型路径/控制路径
    ChatWaifuServer.generateSound(trans, 0, 1, model_path, config_path)
    print("*****************************")
    connection.send(str("finish").encode())
    print("-----------------------------")
    in_path = "test2/game/audio/output.wav"
    out_path = "test2/game/audio/output.ogg"
    sound = AudioSegment.from_wav(in_path)
    sound.export(out_path, format="ogg")