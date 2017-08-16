
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

TOKEN = '447942613:AAE17a-xJ8Aj1CDa28N_SKBY56TckJoyKac'

def print_msg(msg):
    print(json.dumps(msg, indent=4))

def on_chat(msg):
    header = telepot.glance(msg, flavor="chat")
    
    print_msg(msg)

    if header[0] == "text":
        text = msg["text"]
     
        with open('data.json', 'r', encoding='UTF-8') as f:
            data=json.load(f)
        
        image_url = "http://image.knowing.asia/80c5a7af-8c95-4f92-a0bd-58d2fcda2f84/93b20af9836165ddb06c7fa74d78aacd.png"
        for i in data:
            if i['key'] in text:
                image_url = i['value']
                bot.sendPhoto(header[2], image_url)
            
    else: 
        image_url = "http://image.knowing.asia/80c5a7af-8c95-4f92-a0bd-58d2fcda2f84/93b20af9836165ddb06c7fa74d78aacd.png"
        bot.sendPhoto(header[2], image_url)

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {
    'chat': on_chat,
}).run_as_thread()

print('Listening ...')

