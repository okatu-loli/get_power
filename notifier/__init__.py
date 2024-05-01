from .webhook import WebhookNotifier
from .mqtt import MQTTNotifier
from .serverchan import ServerChanNotifier
from .feishu import FeishuNotifier
from .bark import BarkNotifier
from .wechatbot import WeChatBotNotifier


class NotifierFactory:
    notifier_classes = {
        'webhook': WebhookNotifier,
        'mqtt': MQTTNotifier,
        'serverchan': ServerChanNotifier,
        'feishu': FeishuNotifier,
        'bark': BarkNotifier,
        'wechatbot': WeChatBotNotifier
    }

    @staticmethod
    def create_notifier(platform, config_manager):
        notifier_class = NotifierFactory.notifier_classes.get(platform)
        if notifier_class:
            return notifier_class(config_manager)
        else:
            raise ValueError(f"通知渠道 '{platform}' 不受支持.")
