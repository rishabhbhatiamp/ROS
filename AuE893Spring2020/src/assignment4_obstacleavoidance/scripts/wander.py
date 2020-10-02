#!/usr/bin/env python

import rospy
import math
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
global distance_1
global distance_2
global distance_3
global laserscan
distance_1 = 1
distance_2 = 1
distance_3 = 1
global p
p=0

def cal_average(num):
    sum_num = 0
    for t in num:
        sum_num = sum_num + t

    avg = sum_num / len(num)
    return avg

def call_back(msg):
    global laserscan
    global distance_1
    global distance_2
    global distance_3
    distance_1 = []
    distance_2 = []
    distance_3 = []
    laserscan = msg


    for i,value in enumerate(laserscan.ranges):
        if (i <= 30 or i >=330) and value != float('inf'):
            distance_1.append(value)
        if (i>30 and i<=150) and value != float('inf'):
            distance_2.append(value)
        if (i>210 and i<330) and value != float('inf'):
            distance_3.append(value)

    distance_1 = cal_average(distance_1)
    distance_2 = cal_average(distance_2)
    distance_3 = cal_average(distance_3)

if __name__ == '__main__':
    rospy.init_node('wall_follower')
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    follower_subscriber = rospy.Subscriber('/scan' , LaserScan, call_back)
    laserscan = LaserScan()
    vel_msg = Twist()

    rate = rospy.Rate(10)

    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

while not rospy.is_shutdown():
    if distance_1 >=0.4:
        vel_msg.linear.x = 0.3
        p= 0.05

    elif distance_1 < 0.4 and distance_1 > 0.15:
        vel_msg.linear.x = 0.1
        p= 0.2

    str_angle = p*(distance_2 - distance_3)
    vel_msg.angular.z = str_angle
    if distance_1 <= 0.2:
        vel_msg.linear.x = 0.01
        vel_msg.angular.z = 0.2
    print("distance 1- ", distance_1, "disance 2", distance_2, "distance 3- ", distance_3, "streering angle- ", str_angle)
    velocity_publisher.publish(vel_msg)
    rate.sleep()
