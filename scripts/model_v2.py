import rospy #import rospy library
import actionlib #import actionlib to use some action of robot
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Model():

    def __init__(self):

        self.goal_sent = False
        self.index  = 0
        self.goalsBuffer = list()   # list: Danh sach Index cua cac diem
        self.currentGoal = str()    # string: Name of goal that to go
        self.goalReached = 0    # bool
        self.playsoundDone = 0  # bool
        self.goal_data = ''

        # What to do if Shutdown (Ctrl+C, etc)
        rospy.on_shutdown(self.shutdown)

        # initilize action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Wait for the action server to come up")

        # Allow 5 seconds to wait for the action server
        # self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):
        # Send a goal
        self.goal_sent = True

        # Define a new goal
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

        # Send new goal to the system and start to go
        self.move_base.send_goal(goal)

    def cancel(self, clear_buffer = True):
        self.move_base.cancel_all_goals()
        if clear_buffer:
            self.goalsBuffer = [5]
        
    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)


class NewSignal(QObject):
    """define new signal"""
    changed = pyqtSignal(int)

    def __init__(self, x=0):
        QObject.__init__(self)
        self._x = x

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, new_x):
        self._x = new_x
        self.changed.emit(new_x)     