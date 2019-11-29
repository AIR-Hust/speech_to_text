#!/usr/bin/env python
# - *- coding: utf- 8 - *-

import rospy # thu vien ROS cho python
import math # thu vien cac phep toan cho python

from std_msgs.msg import Int32 # loai msg Int32

from geometry_msgs.msg import Twist # message dieu khien robot

# msg ket qua speech to text
from speech_recognition_msgs.msg import SpeechRecognitionCandidates

new_message = False # co soat message

d = 0 # goc quay can thiet robot

# convert degree to radian
def d2r(deg):
    rad = deg*math.pi/180
    print(rad)
    return rad

omega = d2r(30)

# Msg dung robot
stop = Twist()
stop.linear.x = 0; stop.linear.y = 0 ; stop.linear.z = 0
stop.angular.x = 0; stop.angular.y = 0; stop.angular.z = 0

# Msg quay voi toc do goc 5 deg/s
rotate = Twist()
rotate.linear.x = 0; rotate.linear.y = 0 ; rotate.linear.z = 0
rotate.angular.x = 0; rotate.angular.y = 0
rotate.angular.z = omega

rate = 0.1 # tan so gui lenh Twist

# Ham quay mot goc d degree
def rotate_angle(d):
    global new_message
    print(rotate.angular.z)
    #print(rate)
    print(d)
    t = d2r(d)/(omega*rate)
    print("so lan quay")
    print(t)
    new_message = False
    b = 0
    while (b<t):
        rotate.angular.z = - omega # 10*d2r(1)
        print('b') 
        pub.publish(rotate)
        rospy.sleep(rate)
        b = b + 1
        print(b*rate*omega/d2r(1))
        #pub.publish(stop)

    c = 0
    while (c>t):
        rotate.angular.z = omega #10*d2r(-1)
        print('c')
        print(rotate.angular.z)   
        pub.publish(rotate)
        rospy.sleep(rate)
        c = c - 1
        print(c*rate*omega/d2r(1))
    pub.publish(stop)


# Ham callback khi nhan duoc tin hieu huong am thanh
def sound_direction_callback(data):
    global d
    global new_message
    if new_message == False:
        d = float(data.data)
        print(data)
    

def s2t_callback(data):
    global d
    global new_message 
    new_message = True
    print(data)
    if data.transcript == ['hi']:
        print(d)
        rotate_angle(d)
        print('tests2t')
    new_message = False


    

# Chuong trinh chinh
if __name__ == "__main__":
    rospy.init_node('rotate_voice')
    pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
    sub = rospy.Subscriber('/speech_to_text', SpeechRecognitionCandidates, s2t_callback)
    sub = rospy.Subscriber('/sound_direction', Int32, sound_direction_callback)
 
    rospy.spin()
