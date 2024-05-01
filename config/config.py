import configparser


class ConfigManager:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding='utf-8')

    def get(self, section, key):
        return self.config.get(section, key)

    def getbool(self, section, key, default=False):
        """
        获取指定section和key的布尔值。

        :param section: 配置文件中的节（section）名称
        :param key: 要获取的键（key）名称
        :param default: 如果解析失败时返回的默认值，默认为False
        :return: 解析后的布尔值，或在解析失败时返回default值
        """
        value = self.config.get(section, key, fallback=None)  # 使用fallback参数处理键不存在的情况
        if value.lower() in ('true', '1', 'yes'):  # 处理大小写及可能的数字表示
            return True
        elif value.lower() in ('false', '0', 'no'):
            return False
        else:
            # 如果值既不是'true'/'false'等公认布尔表示，也不是数字0/1，
            # 则根据default参数决定返回值
            return default