import requests
import json
from .base_notifier import BaseNotifier


class FeishuNotifier(BaseNotifier):

    def send(self, amt, message):
        url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{self.config.get('Feishu', 'robot_token')}"
        headers = {'Content-Type': 'application/json'}

        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "template": "blue",
                    "title": {
                        "content": "【电费推送】每日电费推送",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "fields": [
                            {
                                "is_short": True,
                                "text": {
                                    "content": "**时间**\n2024年5月1日",
                                    "tag": "lark_md"
                                }
                            },
                            {
                                "is_short": True,
                                "text": {
                                    "content": "**地点**\n星修社工作室",
                                    "tag": "lark_md"
                                }
                            }
                        ]
                    },
                    {
                        "tag": "div",
                        "text": {
                            "content": f"今日查询电费：￥{amt}\n如有疑问，请联系千石：<at id=ou_d1056f135074945213da93073b995207></at>",
                            "tag": "lark_md"
                        }
                    }
                ]
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("电费通知已发送")
        else:
            print("发送电费通知失败")
