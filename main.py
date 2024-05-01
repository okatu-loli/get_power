import time

from playwright.sync_api import sync_playwright

from config.config import ConfigManager
from notifier import NotifierFactory
from scraper.power_scraper import fetch_and_save_qrcode, check_login_success, monitor_electricity_bill, \
    LoginFailedException


def main():
    config = ConfigManager("config.ini")
    platforms = config.get("Notification", "platform").split(',')
    notifiers = [NotifierFactory.create_notifier(platform, config) for platform in platforms] if platforms != [
        ''] else []

    def notify_bill(amount):
        """发送电费通知"""
        message = f"当前电费：{amount}"
        for notifier in notifiers:
            notifier.send(amount, message)

    def notify_err(text, err):
        """发送错误通知"""
        message = f"{text}：{err}"
        for notifier in notifiers:
            notifier.send(None, message)

    max_retries = -1
    retry_delay = 5
    retries = 0
    hours = int(config.get('Notification', 'hours'))
    mins = int(config.get('Notification', 'mins'))

    with sync_playwright() as playwright:
        while max_retries == -1 or retries < max_retries:
            try:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                page.goto("https://95598.cn/osgweb/login")

                fetch_and_save_qrcode(page)

                if check_login_success(page):
                    print("登录成功.")
                    time.sleep(10)

                    # 设置通知回调，用于在监控过程中发送通知
                    monitor_electricity_bill(page, hours=hours, mins=mins, notify_callback=notify_bill)
                    break
                else:
                    raise LoginFailedException("登录失败")
            except LoginFailedException as e:
                print(f"{e}，准备重新尝试...")
                retries += 1
                if retries <= max_retries:
                    print(f"等待{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    notify_err("登录失败", str(e))
            finally:
                # 清理浏览器资源
                if 'page' in locals():
                    page.close()
                if 'context' in locals():
                    context.close()
                if 'browser' in locals():
                    browser.close()

        print("所有尝试均告失败或达到最大重试次数。")


if __name__ == "__main__":
    main()
