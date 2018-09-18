#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
import math

class App:

    def __init__(self, name):
        print("App created!")
        rospy.init_node(name)
        rospy.Subscriber('/odom', Odometry, self.on_odometry_reading)
        rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.on_bump)
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=10)
        self.bumped = False
        self.collissions = []

    def on_odometry_reading(self, msg):
        self.position = msg.pose.pose.position
        self.orientation = msg.pose.pose.orientation

    def on_bump(self, msg):
        print("Bumped into something!")
        self.bumped = True
        self.collissions.append(self.position)
        print(self.collissions)

    def distance(self, a, b):
        return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

    def run(self):
        r = rospy.Rate(10)

        for c in self.collissions:
            if (self.distance(c, self.position) < 1):
                print("Remembered collission!")
                self.bumped = True


        while not rospy.is_shutdown():
            if self.bumped:
                for i in range(0, 10):
                    self.move(-0.2, 0)
                    r.sleep()
                for i in range(0, 15):
                    self.move(0, 1)
                    r.sleep()
                self.bumped = False
            else:
                self.move(0.2, 0)
                r.sleep()
        

    def move(self, speed, angle):
        cmd = Twist()
        cmd.linear.x = speed
        cmd.angular.z = angle
        self.cmd_vel.publish(cmd)
        



    
print("Creating new app...")
x = App("app")
x.run()