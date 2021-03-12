# import execjs

# def get_js():
#     f = open("Samples/GetLocJS.js", 'r', encoding='utf-8')
#     line = f.readline()
#     htmlstr = ''
#     while line:
#         htmlstr = htmlstr+line
#         line = f.readline()
#     return htmlstr

# def get_des_psswd():                                                       
#     js_str = get_js()
#     ctx = execjs.compile(js_str) #加载JS文件
#     return (ctx.call('getLocation'))  #调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数

from urllib.request import urlopen
import json

my_ip = urlopen('http://ip.42.pl/raw').read()
ip_str = str(my_ip.decode())

response = urlopen("https://restapi.amap.com/v3/ip?key=24c1ffc0a6c3d2f1d06570335356875d&ip=" + ip_str)
js = json.load(response)
status = js['status']
if not status == '1':
    print("error")
rect = js['rectangle']
cord_list = rect.split(';')
cord1_long = float(cord_list[0].split(',')[0])
cord1_lan = float(cord_list[0].split(',')[1])
cord2_long = float(cord_list[1].split(',')[0])
cord2_lan = float(cord_list[1].split(',')[1])
cord_cen_long = (cord1_long + cord2_long) / 2
cord_cen_lan = (cord1_lan + cord2_lan) / 2
print(cord_cen_long)
print(cord_cen_lan)

import socket

try: 
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    s.connect(('8.8.8.8',80)) 
    ip = s.getsockname()[0] 
finally: 
    s.close() 
print(ip)  