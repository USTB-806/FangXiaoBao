import asyncio
import websockets
import hmac
import hashlib
import base64
import datetime
import json

# 配置参数
API_KEY = "5b4e5e23"
API_SECRET = "ZmE5OTQzNDM4ODNhZmNkYmM2MzhjMDNl"
APP_ID = "7c525c4baf341120f7f74213445875c7"
HOST_URL = "wss://tts-api.xfyun.cn/v2/tts"

def get_authorization(api_key, api_secret, host_url):
    # 获取当前时间
    date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # 生成签名字符串
    signature_origin = f"host: {host_url.split('//')[1]}\ndate: {date}\nGET /v2/tts HTTP/1.1"
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(signature_sha).decode('utf-8')
    
    # 生成authorization参数
    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
    
    return authorization, date

async def tts_request():
    authorization, date = get_authorization(API_KEY, API_SECRET, HOST_URL)
    url = f"{HOST_URL}?authorization={authorization}&date={date}&host={HOST_URL.split('//')[1]}"
    
    async with websockets.connect(url) as websocket:
        # 发送请求数据
        request_data = {
            "common": {"app_id": APP_ID},
            "business": {"aue": "raw", "vcn": "xiaoyan", "pitch": 50, "speed": 50},
            "data": {"status": 2, "text": base64.b64encode("你好，世界".encode('utf-8')).decode('utf-8')}
        }
        await websocket.send(json.dumps(request_data))
        
        # 接收响应数据
        while True:
            response = await websocket.recv()
            print(response)
            if json.loads(response).get("data", {}).get("status") == 2:
                break

# 运行异步任务
asyncio.get_event_loop().run_until_complete(tts_request())