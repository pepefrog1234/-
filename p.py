#!/usr/bin/python3

import telepot
from bs4 import BeautifulSoup
from telepot.loop import MessageLoop
import time
from pprint import pprint
import os
import requests
import cv2
import threading

bot = telepot.Bot('')
saveDir = '/tmp/hamradio_bot_img/'

prop_day_7 = False
prop_day_14 = False
prop_night_7 = False
prop_night_14 = False

if not os.path.isdir(saveDir):
    os.mkdir(saveDir)

def timer():
    get()
    threading.Timer(3600, timer).start()

def handle(msg):
    if '/getinfo' == msg['text'] or '/getinfo@hamradio_bot' == msg['text']:
        pprint(msg)
        chat_id = msg['chat']['id']
        from_id = msg['from']['id']
        get()
        bot.sendPhoto(chat_id, open(saveDir + 'Congestus_con.jpg', 'rb'))
        cloer()
        ##os.remove('./images/Congestus_con.jpg')
    if '/about' == msg['text'] or '/about@hamradio_bot' == msg['text']:
        pprint(msg)
        chat_id = msg['chat']['id']
        from_id = msg['from']['id']
        bot.sendMessage(chat_id,'本機器人由 BX4ACP 進行開發，為開源免費服務，歡迎大家的使用。\n資料來源：https://rigreference.com/solar\n計畫代號：式神 Project')

def get():  # 圖
    url = 'https://rigreference.com/solar/img/wide'
    response = requests.get(url)  # 使用 header 避免存取受限
    soup = BeautifulSoup(response.content, 'html.parser')
    print("Got pic!\n")
    with open(saveDir + 'Congestus_con.jpg', 'wb') as f:
        f.write(response.content)
    cloer()

def sendmsg(msg):
    print(msg)
    bot.sendMessage(448276213, msg)
    bot.sendMessage(-1001344449061, msg)

def cloer():
    global prop_day_7
    global prop_day_14
    global prop_night_7
    global prop_night_14

    img = cv2.imread(saveDir + 'Congestus_con.jpg')
    (b, g, r) = img[27, 148]  # 7Mhz 日
    if b == 36 and g == 230 and r == 23:
        if prop_day_7 == False:
            sendmsg('7Mhz 白天有傳播！')
            prop_day_7 = True
    else:
        if prop_day_7 == True:
            sendmsg('7Mhz 白天沒傳播了！')
            prop_day_7 = False
    (b, g, r) = img[27, 201]  # 14Mhz 日
    if b == 36 and g == 230 and r == 23:
        if prop_day_14 == False:
            sendmsg('14Mhz 白天有傳播!')
            prop_day_14 = True
    else:
        if prop_day_14 == True:
            sendmsg('14Mhz 白天沒傳播了！')
            prop_day_14 = False
    (b, g, r) = img[72, 149]  # 7Mhz 夜
    if b == 36 and g == 230 and r == 23:
        if prop_night_7 == False:
            sendmsg('7Mhz 晚上有傳播!')
            prop_night_7 = True
    else:
        if prop_night_7 == True:
            sendmsg('7Mhz 晚上沒傳播了！')
            prop_night_7 = False
    (b, g, r) = img[70, 201]  # 14Mhz 夜
    if b == 36 and g == 230 and r == 23:
        if prop_night_14 == False:
            sendmsg('14Mhz 晚上有傳播!')
            prop_night_14 = True
    else:
        if prop_night_14 == True:
            sendmsg('14Mhz 晚上沒傳播了！')
            prop_night_14 = False

MessageLoop(bot, handle).run_as_thread()
print("I'm listening...")
timer()
