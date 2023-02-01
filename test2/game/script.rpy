# 游戏的脚本可置于此文件中。

# 声明此游戏使用的角色。颜色参数可使角色姓名着色。

define e = Character("宁海")
define f = Character("平海")
define config.gl2 = True
image e = Live2D("ninghai_4", top=0.2, base=0.9, height=0.7,loop=True,seamless=True)
image f = Live2D("pinghai_4", top=0.2, base=0.9, height=0.7,loop=True,seamless=True)
define u = Character("User")
# 游戏在此开始。

label start:
    python:
        history = ""
        r = ""
    menu:
        "连续交流":
            jump chat
        "单句交流（线程待修正）":
            jump reply

    # 显示一个背景。此处默认显示占位图，但您也可以在图片目录添加一个文件
    # （命名为 bg room.png 或 bg room.jpg）来显示。
label chat:
    scene 1
    # 显示角色立绘。此处使用了占位图，但您也可以在图片目录添加命名为
    # eileen happy.png 的文件来将其替换掉。
    show e idle
    show f idle
    python:
        import requests
        import threading
        import json
        import re
        import socket
        # 设置你自己的API密匙
        api_key = "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"
        # 设置headers
        headers = {"Authorization": f"Bearer {api_key}"}
        # 设置GPT-3的网址
        api_url = "https://api.openai.com/v1/completions"
        result = ""
        i = 0
        status = 0
        global status
        if status == 0:
            your_text = renpy.input('',length=60)
        prompt = str(your_text)
        # 设置循环可以持续发问
        # 设置请求参数
        all_prompt = history + prompt
        data = {'prompt': all_prompt,
                    "model": "text-davinci-003",
                    'max_tokens': 256,
                    'temperature': 0.9,
                    }
        def get_result():
            global result,i,history,r,status
            response = requests.post(api_url, json=data, headers=headers)
            resp = response.json()
            result = resp["choices"][0]["text"].strip()
            pattern = re.split(r'\n\n',result)  # 查找数字
            pattern = re.split(r'\n', result)  # 查找数字
            if len(pattern)==1:
                r = pattern[0]
                history = history + "Human:" + prompt + "\n" + "AI:" + pattern[0] + "\n"
                status = 2 
            elif len(pattern)==2:
                r = pattern[1]
                history = history + "Human:" + prompt + "\n" + "AI:" + pattern[1] + "\n"
                status = 2 
            elif len(pattern)>2:
                res = ""
                i = 1
                while i<len(pattern):
                    res = str(res) + pattern[i]
                    i = i + 1
                r = res
                history = history + "Human:" + prompt + "\n" + "AI:" + res + "\n"
                status = 2
            else:
                r = "error!"
        thread = threading.Thread(target=get_result)
        thread.start()
    if status == 0 or status == 1:
        $ global status 
        $ status = 1
        show e touch_head idle
        show f touch_head idle
        e "……"
        $ renpy.checkpoint()
        show e mail idle
        show f mail idle
        f "……"
        python:
            if status == 1:
                renpy.rollback(force=False, checkpoints=1, defer=False, greedy=True, label=None, abnormal=True)

    if (status == 2):
        python:
            def voi():
                import socket
                global status
                ip_port = ('127.0.0.1', 9000)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(ip_port)
                data = client.recv(1024)
                if data == b'success':
                    client.send(str(r).encode())
                data = client.recv(1024)
                if data == b'finish':
                    status = 3
            thread2 = threading.Thread(target=voi)
            thread2.start()
        show e touch_head idle
        show f touch_head idle
        e "…"
        $ renpy.checkpoint()
        show e mail idle
        show f mail idle
        f "…"
        python:
            if status == 2:
                renpy.rollback(force=False, checkpoints=1, defer=False, greedy=True, label=None, abnormal=True)

    if (status == 3):
        # 此处显示各行对话。
        voice "audio/output.ogg"
        $ renpy.block_rollback()
        e "[r]"
        voice sustain
        f "准备跳转！"
        menu:
            "继续交流":
                jump chat
            "清除历史":
                python:
                    global history
                    history = ""
                jump chat

    # 此处为游戏结尾。


label reply:
    scene 1
    # 显示角色立绘。此处使用了占位图，但您也可以在图片目录添加命名为
    # eileen happy.png 的文件来将其替换掉。

    show e idle
    show f idle
    $ your_text = renpy.input('',length=60)
    python:
        import requests
        import threading
        import json
        import re

        # 设置你自己的API密匙
        api_key = "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"
        # 设置headers
        headers = {"Authorization": f"Bearer {api_key}"}
        # 设置GPT-3的网址
        api_url = "https://api.openai.com/v1/completions"
        result = ""
        i = 0
        prompt = str(your_text)
        # 设置循环可以持续发问
        # 设置请求参数
        data = {'prompt': all_prompt,
                    "model": "text-davinci-003",
                    'max_tokens': 512,
                    'temperature': 0.9,
                    }
        def get_result():
            global result,i,history,r
            response = requests.post(api_url, json=data, headers=headers)
            resp = response.json()
            result = resp["choices"][0]["text"].strip()
            pattern = re.split(r'\n\n',result)  # 查找数字
            pattern = re.split(r'\n', result)  # 查找数字
            if len(pattern)==1:
                r = pattern[0]
            elif len(pattern)==2:
                r = pattern[1]
            elif len(pattern)>2:
                res = ""
                i = 1
                while i<len(pattern):
                    res = str(res) + pattern[i]
                    i = i + 1
                r = res
            else:
                r = "error!"
        get_result()
    # 此处显示各行对话。
    # 此处显示各行对话。
    show e mail idle
    show f mail idle
    u "[prompt]"
    f "[r]"
    show e touch_head idle
    show f touch_head idle
    e "准备跳转！"
    jump reply

   
