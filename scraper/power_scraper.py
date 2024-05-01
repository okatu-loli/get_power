import base64
import os
import time
from datetime import datetime, timedelta

from playwright.sync_api import expect

QR_CODE_PATH = "qrcode/qrcode.png"
WAIT_TIMEOUT = 1000000


def ensure_directory_exists(file_path):
    """确保文件路径的目录存在"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)


def save_qrcode_as_image(base64_data, path):
    """保存Base64编码的图片到指定路径"""
    image_data = base64.b64decode(base64_data)
    with open(path, 'wb') as file:
        file.write(image_data)


def fetch_and_save_qrcode(page):
    """获取并保存二维码到本地"""
    qrcode_locator = page.locator(".sweepCodePic .el-tooltip.imgLogin")
    expect(qrcode_locator).to_be_visible(timeout=WAIT_TIMEOUT)
    page.wait_for_function(
        "() => document.querySelector('.sweepCodePic .el-tooltip.imgLogin').src.startsWith('data:image')",
        timeout=WAIT_TIMEOUT)

    img_data_url = qrcode_locator.get_attribute('src')
    if img_data_url and img_data_url.startswith('data:image'):
        img_base64 = img_data_url.split(',', 1)[1]
        save_qrcode_as_image(img_base64, QR_CODE_PATH)
        print(f'二维码保存到 {QR_CODE_PATH}')
    else:
        raise LoginFailedException("无法获取有效的二维码图像")


def check_login_success(page):
    """检查登录是否成功"""
    login_indicator = "#member_info > div > div > div > div > div.outerLayer > ul > li.content-name"
    page.wait_for_selector(login_indicator, timeout=WAIT_TIMEOUT)
    return page.is_visible(login_indicator)


def get_and_print_electricity_bill(page):
    """获取并打印电费信息"""
    bill_selector = ('#app > div > div > article > div > div > div.content-row.load-after-box > '
                     'div > div > div > div > div > '
                     'div.el-col.el-col-24.el-col-md-18.el-col-lg-19.el-col-xl-19 > div > div > div > '
                     'div.center_menu_t > ul > li > div.content > p:nth-child(2) > b')
    try:
        time.sleep(10)
        page.wait_for_selector(bill_selector, timeout=WAIT_TIMEOUT)
        electricity_bill = page.inner_text(bill_selector)
        print("当前电费:", electricity_bill)
        return electricity_bill
    except Exception as e:
        print(f"获取电费信息失败: {e}")


def should_refresh_at_specific_time(hours, mins):
    """判断当前时间是否达到指定的小时和分钟进行刷新"""
    now = datetime.now()
    target_time = now.replace(hour=hours, minute=mins, second=0, microsecond=0)
    if now > target_time:
        # 如果当前时间已经超过设定的时间，则安排到明天的同一时间
        target_time += timedelta(days=1)
    return now >= target_time


def monitor_electricity_bill(page, hours, mins, notify_callback=None):
    """监控电费信息并在指定时间刷新页面"""
    last_check_time = None  # 初始化上次检查时间
    while True:
        now = datetime.now()

        # 首次运行或达到刷新间隔，刷新页面并检查登录状态
        if hours and mins and should_refresh_at_specific_time(hours, mins):
            print(f"到达指定刷新时间({now.strftime('%Y-%m-%d %H:%M:%S')})，刷新页面...")
            page.reload()

            while True:
                bill_selector = (
                    '#app > div > div > article > div > div > div.content-row.load-after-box > div > div > div > '
                    'div > div > div.el-col.el-col-24.el-col-md-18.el-col-lg-19.el-col-xl-19 > div > div > div > '
                    'div.center_menu_t > ul > li:nth-child(2) > div.content > p > b')
                element = page.query_selector(bill_selector)

                if element:
                    # 获取元素的文本内容
                    text_content = element.text_content()

                    # 判断文本内容是否以"--"开头
                    if not text_content.startswith("--"):
                        print("元素的文本内容不以'--'开头，停止循环。")
                        break
                    else:
                        print("元素的文本内容仍然以'--'开头，10秒后重试。")
                else:
                    print("未找到指定的元素，10秒后重试。")

                # 等待10秒
                time.sleep(10)

                # 刷新页面
                page.reload()

            if not check_login_success(page):
                print("登录失效，监控结束。")
                break

        # 尝试获取并处理电费信息
        try:
            electricity_bill = get_and_print_electricity_bill(page)
            if electricity_bill:
                print(f"当前电费：{electricity_bill}元")
                if notify_callback:
                    notify_callback(electricity_bill)  # 调用通知回调
        except Exception as e:
            print(f"获取电费信息失败: {e}")

        # 等待直到下一次检查
        wait_until_next_refresh = (now.replace(hour=hours, minute=mins, second=0, microsecond=0) - now).total_seconds()
        if wait_until_next_refresh <= 0:  # 如果已经过了今天特定时间，等待到明天
            wait_until_next_refresh += timedelta(days=1).total_seconds()
        time.sleep(wait_until_next_refresh)


# 定义自定义异常类
class LoginFailedException(Exception):
    """登录失败异常"""

    def __init__(self, message="登录过程中出现问题"):
        super().__init__(message)
