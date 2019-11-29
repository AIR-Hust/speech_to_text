#!/usr/bin/env python
# - *- coding: utf- 8 - *-

import rospy # thu vien ROS cho python
import math # thu vien cac phep toan cho python

from std_msgs.msg import Int32 # loai msg Int32

from geometry_msgs.msg import Twist # message dieu khien robot
from nav_msgs.msg import Odometry

# msg ket qua speech to text
from speech_recognition_msgs.msg import SpeechRecognitionCandidates

new_message = False # co soat message

d = 0 # goc quay can thiet robot
odom_z = 0

# convert degree to radian
def d2r(deg):
    rad = deg*math.pi/180
    print(rad)
    return rad

omega = d2r(30)

# Function to convert quaternion to euler
def quaternion_to_euler(x, y, z, w):

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch = math.asin(t2)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)
    return [yaw, pitch, roll]

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

# Ham odom callback
def odom_callback(data):
    odom = quaternion_to_euler(data.pose.pose.orientation)

# Ham quay mot goc d degree
def rotate_angle(d):
    global new_message
    print(rotate.angular.z)
    #print(rate)
    print(d)
    odom_goal = d2r(d) + odom[roll]
    #if odom_goal > math.pi:
     #   odom_goal = odom_goal - 2*math.pi


    print("so lan quay")
    print(t)
    new_message = False
    b = 0
    if d>0:
        while (odom[roll] < odom_goal):
            rotate.angular.z = - omega # 10*d2r(1)
            print('b') 
            pub.publish(rotate)
            rospy.sleep(rate)
            #b = b + 1
            #print(b*rate*omega/d2r(1))
            #pub.publish(stop)

    c = 0
    if d<0:
        while (odom[roll] > odom_goal):
            rotate.angular.z = omega #10*d2r(-1)
            print('c')
            #print(rotate.angular.z)   
            pub.publish(rotate)
            rospy.sleep(rate)
            #c = c - 1
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
    sub1 = rospy.Subscriber('/speech_to_text', SpeechRecognitionCandidates, s2t_callback)
    sub2 = rospy.Subscriber('/sound_direction', Int32, sound_direction_callback)
    sub3 = rospy.Subscriber('/odom', Odometry, odom_callback)
 
    rospy.spin()
