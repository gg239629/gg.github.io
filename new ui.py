from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# 替换为你的API Key和Secret Key
API_KEY = 'Gk1EtblV8UgRnZbiL4f6jF7i'  # 你的API Key
SECRET_KEY = 'oIT278La50kvMKF54t4MmXGguvnTpwe1'  # 你的Secret Key


def get_access_token():
    """获取Access Token"""
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"

    try:
        response = requests.post(url)
        response.raise_for_status()  # 确保请求成功
        return response.json().get("access_token")
    except Exception as e:
        print(f"获取 Access Token 失败: {e}")
        return None


@app.route('/')
def index():
    return render_template('intex.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    token = get_access_token()

    if not token:
        return jsonify({"response": "无法获取Access Token，无法进行聊天."})

    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-pro-128k?access_token={token}"

    payload = json.dumps({
        "messages": [{"role": "user", "content": user_input}]
    })

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # 确保请求成功
        json_result = response.json()

        if 'result' in json_result:
            return jsonify({"response": json_result['result']})
        else:
            return jsonify({"response": "未找到结果."})
    except Exception as e:
        return jsonify({"response": f"请求失败: {e}"})


if __name__ == '__main__':
    app.run(debug=True)
