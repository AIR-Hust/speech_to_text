#!/usr/bin/env python
# -*- coding: utf8 -*-

import rospy
import math
import os
import yaml
import time
import sys, select, termios, tty
from geometry_msgs.msg import Twist
from GoToPose import GoToPose
from model_v2 import Model
# msg ket qua speech to text
from speech_recognition_msgs.msg import SpeechRecognitionCandidates

model = Model()

msg = """
Control Your Cbot!
---------------------------
Moving around:
đi thẳng
lùi lại
quay phải 
quay trái
dừng lại
"""

moveBindings = {
        'đi thẳng':(1,0),
        'Đi thẳng':(1,0),
        'Đi Thẳng':(1,0),
        'lùi lại':(-1,0),
        'Lùi lại':(-1,0),
        'Lùi Lại':(-1,0),
        'quay phải':(0,-1),
        'Quay phải':(0,-1),
        'Quay Phải':(0,-1),
        'quay trái':(0,1),
        'Quay trái':(0,1),
        'quay Trái':(0,1),
           }

speed = 0.12 # m/s
turn = 1 # rad/s

# Gan toc do ban dau cho robot
x = 0 # toc do dai
a = 0 # toc do goc
target_speed = 0
target_turn = 0


twist = Twist()
twist.linear.x = target_speed; twist.linear.y = 0 ; twist.linear.z = 0
twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = target_turn
 
stop = Twist()
stop.linear.x = 0; stop.linear.y = 0 ; stop.linear.z = 0
stop.angular.x = 0; stop.angular.y = 0; stop.angular.z = 0


def s2t_callback(data):
    global s2t
    global x, a
    global speed, turn
    global twist
    print(unicode(data.transcript[0],'utf-8'))
    #word = unicode(data.transcript[0],'utf-8')
    word = data.transcript[0]

    for obj in dataMap:
        #name = obj['name']
        #print(type(obj['name']))
        if (unicode(word,'utf-8') == obj['name']):
            # Navigation
            #rospy.loginfo("Go to %s pose", name[:-4])
            #success = navigator.goto(obj['position'], obj['quaternion'])
            model.goto(obj['position'], obj['quaternion'])
            #if not success:
                #rospy.loginfo("Failed to reach %s pose", name[:-4])
             #   continue
            #rospy.loginfo("Reached %s pose", name[:-4])
    if (word == 'dừng lại'):
        pub.publish(stop)
        rospy.sleep(1)
    elif word in moveBindings.keys():
        x = moveBindings[word][0]
        a = moveBindings[word][1]
    else:
        x = 0
        a = 0

    target_speed = speed * x
    print(target_speed)
    target_turn = turn * a
    twist.linear.x = target_speed; twist.angular.z = target_turn
    print(twist)
    pub.publish(twist)
    rospy.sleep(1)
    #pub.publish(stop)


if __name__ == '__main__':

    # Read information from yaml file
    with open("route.yaml", 'r') as stream:
        dataMap = yaml.load(stream)

    rospy.init_node("voice_teleop", anonymous=True)
    pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
    sub = rospy.Subscriber('/speech_to_text', SpeechRecognitionCandidates, s2t_callback)
    navigator = GoToPose()
    






    rospy.spin()