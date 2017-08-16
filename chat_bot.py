
# coding: utf-8

# In[3]:

# import 一大堆lib
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from random import choice
import json


# In[5]:

# 記得改token
# 記得改token
# 記得改token
TOKEN = input("Please input your bot token")


# In[8]:

def print_msg(msg):
    print(json.dumps(msg, indent=4))

def on_chat(msg):
    header = telepot.glance(msg, flavor="chat")
    
    print_msg(msg)

    if header[0] == "text":
        text = msg["text"]
        
        # 當開頭有"/"時，忽略掉它
        if text.startswith("/"):
            command = text.lstrip("/")
            
            # Let's START!!
            if command == "start":
                text = '想跟人起爭議嗎？找"圖戰機器人"吧！'
                bot.sendMessage(header[2], text)
        # other msg
            elif command == '黑人問號':
                image_url = "http://i.imgur.com/u4N3wpJ.jpg"
                bot.sendPhoto(header[2], image_url)
        else: 
            # 你在工殺小
            image_url = "https://i.imgur.com/64rWKQWl.jpg"
            bot.sendPhoto(header[2], image_url)


# In[9]:

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {
    'chat': on_chat
}).run_as_thread()

print('Listening ...')

