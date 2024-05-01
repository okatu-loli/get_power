import requests
import json
from .base_notifier import BaseNotifier


class WeChatBotNotifier(BaseNotifier):
    def send(self, amt, message):
        url = f"{self.config.get('WeChatBot', 'url')}/webhook/msg/v2?token={self.config.get('WeChatBot', 'token')}"
        print(url)
        headers = {'Content-Type': 'application/json'}
        payload = {
            "to": self.config.get('WeChatBot', 'to'),
            "isRoom": self.config.getbool('WeChatBot', 'isRoom'),
            "data": {"content": f"{message}"}
        }
        print("request.data:", json.dumps(payload))
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print('电费通知已发送')
        else:
            print('发送电费通知失败')
