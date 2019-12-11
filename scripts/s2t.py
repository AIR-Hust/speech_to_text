#!/usr/bin/env python
# -*- coding: utf8 -*-

import rospy

# msg ket qua speech to text
from speech_recognition_msgs.msg import SpeechRecognitionCandidates

def s2t_callback(data):
    print(unicode(data.transcript[0],'utf-8'))


if __name__ == '__main__':
    rospy.init_node("Speech_to_text")
    sub = rospy.Subscriber('/speech_to_text', SpeechRecognitionCandidates, s2t_callback)
    rospy.spin()