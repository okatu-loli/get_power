# GetPower 项目文档

**有问题可以进QQ群交流：361997678**

## 简介

**GetPower** 是一个实用的小工具，旨在帮助用户实时监控和通知电费情况。该工具支持通过二维码登录，并能将电费信息推送至多个平台，包括飞书、MQTT、ServerChan、微信机器人Webhook、Webhook以及Bark。

## 特性

- **支持多种通知平台**：飞书、MQTT、ServerChan、wechatbot-Webhook、Webhook和Bark。
- **二维码登录**：简便快捷的二维码登录方式。
- **定时推送**：可配置的推送时间，按时提醒电费信息。

## 快速开始

### 1. 配置环境

首先，确保你的系统中已安装了Python和所需的依赖。
```
git clone https://github.com/okatu-loli/get_power
pip install -r requirements.txt
# python -m playwright install
playwright install
```

### 2. 配置文件

复制 `config.ini.example` 文件并重命名为 `config.ini`，根据需要填写以下配置信息：

```plaintext
[Notification]
; 可选平台：feishu, serverchan, mqtt, webhook, bark。多个平台启用时用逗号隔开
platform =
hours = 14
mins = 00

[ServerChan]
; Server酱发送密钥
send_key =

[Feishu]
; 飞书机器人token
robot_token =

[Webhook]
; Webhook URL
webhook_url =

[MQTT]
; Mqtt的地址
mqtt_host =
mqtt_port =
mqtt_topic =

[Bark]
url =
token =

[WeChatBot]
url =
token =
to =
isRoom =
```

### 3. 启动程序

启动程序后，访问 `http://你的IP:5000/qrcode`，扫描二维码进行登录。

## 注意事项

- 如果访问二维码页面时提示404，或扫描二维码后提示失效，请检查程序控制台的日志输出。
- 二维码检测可能存在5-10秒的延迟，二维码失效会在日志中有所提示。

## TODO

- [ ] 支持多户号

## 贡献

如果你在使用过程中遇到任何问题，欢迎提Issue。同时，我们也欢迎各种Pull Requests。

## 免责声明

本工具仅供学习交流使用，请勿用于商业用途，请在下载后24小时内删除。
