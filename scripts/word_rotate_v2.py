#!/usr/bin/env python
# - *- coding: utf- 8 - *-

import rospy # thu vien ROS cho python
import math # thu vien cac phep toan cho python

from std_msgs.msg import Int32 # loai msg Int32

from geometry_msgs.msg import Twist # message dieu khien robot
from nav_msgs.msg import Odometry # msg of Odom topic

# msg result of speech to text
from speech_recognition_msgs.msg import SpeechRecognitionCandidates

new_message = False # co soat message

d = 0 # goc quay can thiet robot
odom = [] # Roll pitch yaw at realtime

# convert degree to radian
def d2r(deg):
    rad = deg*math.pi/180
    print(rad)
    return rad

omega = d2r(30) # Toc do goc quay robot

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
    return [roll, pitch, yaw]

# Msg dung robot
stop = Twist()
stop.linear.x = 0; stop.linear.y = 0 ; stop.linear.z = 0
stop.angular.x = 0; stop.angular.y = 0; stop.angular.z = 0

# Msg quay voi toc do goc 30 deg/s
rotate = Twist()
rotate.linear.x = 0; rotate.linear.y = 0 ; rotate.linear.z = 0
rotate.angular.x = 0; rotate.angular.y = 0
rotate.angular.z = omega

rate = 0.1 # tan so gui lenh Twist

# Ham odom callback
def odom_callback(data):
    global odom
    orien_x = data.pose.pose.orientation.x
    orien_y = data.pose.pose.orientation.y
    orien_z = data.pose.pose.orientation.z
    orien_w = data.pose.pose.orientation.w
    odom = quaternion_to_euler(orien_x, orien_y, orien_z, orien_w)

# Ham quay mot goc d degree
def rotate_angle(d):
    global new_message
    #print(rotate.angular.z)
    print(d)
    odom_goal = d2r(d) + odom[2] # The goal angle
    print(odom[2])
    print('goal: ')
    print(odom_goal)

    # First case
    if (odom_goal > math.pi) & (d > 0):
        odom_goal = odom_goal - 2*math.pi
        print('recal')
        print(odom_goal)
        while (odom[2] < math.pi) & (odom[2] > 0):
            rotate.angular.z = omega
            print('cw') 
            pub.publish(rotate)
            rospy.sleep(rate)
        while (odom[2] > -math.pi) & (odom_goal > odom[2]):
            rotate.angular.z = omega
            print('cw')  
            pub.publish(rotate)
            rospy.sleep(rate)

    # Second case
    if (odom_goal < -math.pi) & (d<0):
        odom_goal = odom_goal + 2*math.pi
        print("recalculate")
        print(odom_goal)
        while (odom[2] > -math.pi) & (odom[2] < 0):
            rotate.angular.z = -omega 
            print('ccw')  
            pub.publish(rotate)
            rospy.sleep(rate)
        while (odom[2] < math.pi) & (odom_goal < odom[2]):
            rotate.angular.z = -omega
            print('ccw')  
            pub.publish(rotate)
            rospy.sleep(rate)

    if d>0:
        while (odom[2] < odom_goal):
            rotate.angular.z = omega 
            print('cw') 
            pub.publish(rotate)
            rospy.sleep(rate)

    if d<0:
        while (odom[2] > odom_goal):
            rotate.angular.z = -omega 
            print('ccw') 
            pub.publish(rotate)
            rospy.sleep(rate)
    print("Final: ")
    print(odom[2])
    pub.publish(stop)

# Ham callback khi nhan duoc tin hieu huong am thanh
def sound_direction_callback(data):
    global d
    global new_message
    if new_message == False:
        d = -float(data.data) # Do goc microphone array nguoc chieu voi goc odom
        print(data)
    

def s2t_callback(data):
    global d
    global new_message 
    new_message = True
    print(data)
    if data.transcript == ['hi']: # 'hi' is the wake up word
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
