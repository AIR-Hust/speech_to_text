#!/usr/bin/env python
# encoding: utf-8

import requests
#import os
import json

#file_name = "/home/tungngo/catkin_ws/src/speech_to_text/voice"
url = 'https://api.fpt.ai/hmi/asr/general'
headers = {
    'api-key': 'rmm5sVL4GayFCrbVJbO3YtEocDgSJsO7'
}

payload = open("/home/tungngo/catkin_ws/src/speech_to_text/output.wav", 'rb').read()
        
response = requests.post(url=url, data=payload, headers=headers)

print(response.json())

with open('json_file.json', "w") as file_write:
    json.dump(response.json(), file_write)


'''
for root, dirs, files in os.walk(file_name):
    #if name in files:
    print(files)
    print(len(files))
    for i in range(len(files)):
        audio_file = file_name + "/" + files[i]
        print(audio_file)
        payload = open(audio_file, 'rb').read()
        
        response = requests.post(url=url, data=payload, headers=headers)

        print(response.json())
'''
