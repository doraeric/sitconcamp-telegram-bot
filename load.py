import json

with open('data.json', 'r', encoding='UTF-8') as f:
    data=json.load(f)

text = "害怕"
for i in data:
    if i['key'] in text:
        image_url = i['value']
#         bot.sendPhoto(header[2], image_url)