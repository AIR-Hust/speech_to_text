#!/usr/bin/env python
# - *- coding: utf- 8 - *-

import rospy # thu vien ROS cho python
import math

from std_msgs.msg import Int32 

from geometry_msgs.msg import Twist # message dieu khien robot

new_message = True # False

global d
d = 0

# convert degree to radian
def d2r(deg):
    rad = deg*math.pi/180
    return rad


stop = Twist()
stop.linear.x = 0; stop.linear.y = 0 ; stop.linear.z = 0
stop.angular.x = 0; stop.angular.y = 0; stop.angular.z = 0

rotate = Twist()
rotate.linear.x = 0; rotate.linear.y = 0 ; rotate.linear.z = 0
rotate.angular.x = 0; rotate.angular.y = 0; rotate.angular.z = 5*d2r(1)

rate = 0.1

def rotate():
    while(new_message == False):
        t = d2r(d)/(rotate.angular.z*rate)
        print(t)
        new_message = False
        b = 0
        while (b<t):
            if new_message == False:   
                pub.publish(rotate)

                rospy.sleep(rate)
                b = b + 1
                print(b*rate)
                #pass
                pub.publish(stop)

        c = 0
        while (c>t):
            if new_message == False:
                rotate.angular.z = 5*d2r(-1)   
                pub.publish(rotate)

                rospy.sleep(rate)
                c = c - 1
                print(c*rate)
                #pass
                pub.publish(stop)

# Ham callback khi nhan duoc tin hieu huong am thanh
def callback(data):
    new_message = True
    d = float(data.data)
    print(data)
    data = float(data.data)
    
    #print(rotate.angular.z)
    
    if new_message == False:
        rotate()
    new_message = False
    
    

# Chuong trinh chinh
if __name__ == "__main__":
    #init()
    rospy.init_node('rotate_voice')
    #pub = rospy.Publisher('~cmd_vel', Twist, queue_size=5)
    pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=5)
    #callback(90)
    sub = rospy.Subscriber('/sound_direction', Int32, callback)

    print('d:')
    print(d)
    
    

    rospy.spin()
