import rospy
import math

from nav_msgs.msg import Odometry

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

def odom_callback(data):
    global odom
    orien_x = data.pose.pose.orientation.x
    orien_y = data.pose.pose.orientation.y
    orien_z = data.pose.pose.orientation.z
    orien_w = data.pose.pose.orientation.w
    odom = quaternion_to_euler(orien_x, orien_y, orien_z, orien_w)
    print(odom)

if __name__ == "__main__":
    rospy.init_node('quaternion_to_euler')
    sub3 = rospy.Subscriber('/odom', Odometry, odom_callback)
    rospy.spin()