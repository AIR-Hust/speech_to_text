#!/usr/bin/env python
# encoding: utf-8
import requests
import os

import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

print('recording')
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording)  # Save as WAV file 

file_name = "/home/tungngo/catkin_ws/src/speech_to_text/voice"
url = 'https://api.fpt.ai/hmi/asr/general'
headers = {
    'api-key': '3D6Z5YgByp3P5E2UWQN1o3QLVtQiF6ap'
}

payload = open("/home/tungngo/catkin_ws/src/speech_to_text/output.wav", 'rb').read()
        
response = requests.post(url=url, data=payload, headers=headers)

print(response.json())

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