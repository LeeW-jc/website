import time
import random


def log(*args, **kwargs):
    dt = time.localtime(int(time.time()))  # time.time()为微秒时间戳，time.localtime()为时间元组
    dt_format = "%Y-%m-%d %H:%M:%S"  # time.strftime(参数1， 参数2) 参数1为格式str，参数2为时间元组
    DT = time.strftime(dt_format, dt)
    with open("log_utils.txt", "a", encoding="utf-8") as f:
        print(DT, *args, file=f, **kwargs)


def format_content(content):
    a = content.replace(' ', '&nbsp')
    b = a.replace('<', '&lt')
    c = b.replace('>', '&gt')
    d = c.replace('\r\n', '<br>')
    e = d.replace('\n', '<br>')
    return e


def random_background():
    background = {
        1: "#FCE6C9",
        2: "#708069",
        3: "#B03060",
        4: "#872657",
        5: "#BDFCC9",
        6: "#E3CF57",
        7: "#082E54",
        8: "#3D9140",
        9: "#A066D3",
        10: "#873324",
        11: "#FF7D40",
        12: "#33A1C9",
    }
    return background[random.randint(1, 12)]


style = ['background: #03e9f4;color: #000;'
         'box-shadow: 0 0 5px #03e9f4,0 0 25px #03e9f4,0 0 50px #03e9f4,0 0 200px #03e9f4;',
         'background: #FF8C00;color: #000;box-shadow: 0 0 5px #FF8C00,'
         '0 0 25px #FF8C00,0 0 50px #FF8C00,0 0 200px #FF8C00;']
