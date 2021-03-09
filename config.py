import configparser
import os
from PIL import Image
import qrcode

path = "config.conf"

def get_config(section, key):
    config = configparser.ConfigParser()
    config.read(path)
    return config.get(section, key)

def set_config(section, key, content):
    config = configparser.ConfigParser()
    config.read(path)
    config.set(section, key, content)
    with open(path, 'w') as conf:
        config.write(conf)

# 设置景点id
def set_spot_id(idn):
    set_config("robotinfo", "spotid", str(idn))

# 获取地图链接
def get_map_url():
    map_url = get_config("robotinfo", "mapurl") + get_config("robotinfo", "spotid")
    return map_url

# 设置机器人id
def set_robot_id(idn):
    set_config("robotinfo", "robotid", str(idn))

# 获取机器人id
def get_robot_id():
    return get_config("robotinfo", "robotid")

# 获取机器人二维码
def get_robot_qrcode():
    qrcode_path = "resources/qrcode.png"
    robot_qrcode_url = get_config("robotinfo", "roboturl") + get_config("robotinfo", "robotid")
    qr = qrcode.QRCode(
    version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=4, border=4)
    qr.add_data(robot_qrcode_url)
    qr.make(fit=True)

    img = qr.make_image()
    img = img.convert("RGBA")

    icon = Image.open("resources/logo.png")  # 这里是二维码中心的图片

    img_w, img_h = img.size
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    icon = icon.convert("RGBA")
    img.paste(icon, (w, h), icon)
    img.save(qrcode_path)
    return qrcode_path

# Test Demo
if __name__ == '__main__':
    # print("QRCode url:{}".format(get_config("robotinfo", "roboturl")))
    # set_config("robotinfo", "robotid", "12345")
    # print("QRCode url:{}".format(get_config("robotinfo", "roboturl") + get_config("robotinfo", "robotid")))
    print("map url:{}".format(get_map_url()))
    set_robot_id(23383)
    print("robot id: {}".format(get_robot_id()))
    qr_url = get_robot_qrcode()
    print(qr_url)
    