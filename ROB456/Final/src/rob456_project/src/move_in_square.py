#!/usr/bin/env python

#import relevant libraries
import roslib
import rospy
import math

# The geometry_msgs Twist message
from geometry_msgs.msg import Twist

#the move_base result message
from move_base_msgs.msg import MoveBaseActionResult

def mb_callback(msg):
  #Check if robot has reached goal
  if msg.status.status == 2 or msg.status.status == 4 or msg.status.status == 5 or msg.status.status ==6:
    print "Robot failed to reach waypoint!"
  elif msg.status.status == 3:
    print "Robot successfully reached waypoint!"

  #Make a new Twist waypoint message
  waypoint = Twist()

  #command waypoint 20 units to the right of the current robot position
  waypoint.linear.x = 0.0
  waypoint.linear.y = -20.0
  waypoint.linear.z = 0.0

  #Command the robot to turn90 degrees clockwise
  waypoint.angular.x = 0.0
  waypoint.angular.y = 0.0
  waypoint.angular = -90.0

  pub.publish(waypoint)
    


if __name__ == "__main__":
  #initialize the node
  rospy.init_node('move_in_square')
  
  #publish waypoint data to root
  pub = rospy.Publisher('/base_link_goal',Twist,queue_size=10)

  #subscribe to move_base result
  sub = rospy.Subscriber('/move_base/result',MoveBaseActionResult, mb_callback)

  #turn control to ROS
  rospy.spin()


