#!/usr/bin/env python

import rospy
import math
import tf
from tf.transformations import euler_from_quaternion
import message_filters
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#import time

# The laser scan message
from sensor_msgs.msg import LaserScan

# The odometry message
from nav_msgs.msg import Odometry

# the velocity command message
from geometry_msgs.msg import Twist

# instantiate global variables "globalOdom"
globalOdom = Odometry()

# global pi - this may come in handy
pi = math.pi

#Start matplotlib
#fig = plt.figure()
#ax = fig.add_subplot(111)
#li, = ax.plot([],[])
#ax.relim()
#ax.autoscale_view(True,True,True)
#fig.canvas.draw()
#plt.show(block = False)

# method to control the robot
def callback(scan,odom):
    # the odometry parameter should be global
    global globalOdom
    globalOdom = odom

    # make a new twist message
    command = Twist()

    # Fill in the fields.  Field values are unspecified 
    # until they are actually assigned. The Twist message 
    # holds linear and angular velocities.
    command.linear.x = 0.0
    command.linear.y = 0.0
    command.linear.z = 0.0
    command.angular.x = 0.0
    command.angular.y = 0.0
    command.angular.z = 0.0

    # get goal x and y locations from the launch file
    goalX = rospy.get_param('hw2/goalX',0.0)
    goalY = rospy.get_param('hw2/goalY',0.0)
    
    # find current (x,y) position of robot based on odometry
    currentX = globalOdom.pose.pose.position.x
    currentY = globalOdom.pose.pose.position.y

    # find current orientation of robot based on odometry (quaternion coordinates)
    xOr = globalOdom.pose.pose.orientation.x
    yOr = globalOdom.pose.pose.orientation.y
    zOr = globalOdom.pose.pose.orientation.z
    wOr = globalOdom.pose.pose.orientation.w

    # find orientation of robot (Euler coordinates)
    (roll, pitch, yaw) = euler_from_quaternion([xOr, yOr, zOr, wOr])

    # find currentAngle of robot (equivalent to yaw)
    # now that you have yaw, the robot's pose is completely defined by (currentX, currentY, currentAngle)
    #Changed this to be from 0 to 2*pi, Worker better mathmatically
    #if yaw > 0:    
    currentAngle = yaw
    #if yaw < 0:
     # currentAngle = yaw + 2 * pi        

    # find laser scanner properties (min scan angle, max scan angle, scan angle increment)
    maxAngle = scan.angle_max
    minAngle = scan.angle_min
    angleIncrement = scan.angle_increment

    # find current laser angle, max scan length, distance array for all scans, and number of laser scans
    currentLaserTheta = minAngle
    maxScanLength = scan.range_max 
    distanceArray = scan.ranges
    numScans = len(distanceArray)
   
    # the code below (currently commented) shows how 
    # you can print variables to the terminal (may 
    # be useful for debugging)
    #print 'x: {0}'.format(currentX)
    
    #Turning Posistion into vector for easy access
    currentPos = np.array([currentX,currentY])
    goalPos = np.array([goalX,goalY])
  
    #Turns Robot Towards a point
    #Could be inproved, doesn't take in account shortest path
    #eg: going from - pi to pi does a full revolution. 
    #Could change this by checking for the shortest path
    def turnRobot(target): 
      dirVec = target - currentPos
      tol = .01
      rotSpeed = 1
      goalAngle = np.arctan(dirVec[1]/dirVec[0])
      #print 'y/x: {0}'.format(dirVec[1]/dirVec[0])
      if dirVec[0] < 0.0 and dirVec[1] < 0.0: #Accounting for acrtan domain/range problems
        goalAngle = goalAngle - pi
      if dirVec [0] < 0.0 and dirVec[1] > 0.0:
        goalAngle = goalAngle + pi
      if abs(currentAngle - goalAngle) > tol:
        command.angular.z = (-currentAngle + goalAngle) * rotSpeed
        
    wayPoint = goalPos
    # for each laser scan
    resetWp = False
    for curScan in range(0, numScans):
        # curScan (current scan) loops from 0 to 
        # numScans (length of vector containing laser range data)
        # for each laser scan, the angle is currentLaserTheta,
        # and the range is distanceArray[curScan]
        #Check if anything is in our way  
    
    
       
        # after you are done using one laser scan, update 
        # the current laser scan angle before the for loop
        # is incremented
          currentLaserTheta = currentLaserTheta + angleIncrement
          
          
          fov = pi/3 # The feild of veiw that the robot is worried about
          minDist = 2 #Distance from the robot the object has to be before it makes an action
          if -fov < currentLaserTheta < fov and resetWp == False:
            if distanceArray[curScan] < (minDist * (fov - abs(currentLaserTheta)) +.5):
              resetWp = True
              
              
              
              
    #Setting New waypoint to not hit objects
    #Doesn't take into account where the actual goal is, moving out of walls is first prioirty
    #Something is wrong with the wall detection? moves from blocks fine
    #If the whoel area is wall, should move towards furthest point?
    offSet = 0 #How much it decides to turn    
    if resetWp:
      for i in range(0,numScans/2):
        if distanceArray[numScans/2 + i] > 5: #Checking to the left
          theta = minAngle + (numScans/2 + i + offSet)*angleIncrement
          d = distanceArray[numScans/2 + i]
          wpRel = np.array(np.cos(theta) * d, np.sin(theta) * d)
          wayPoint = (currentPos + wpRel)
          print('left')
          resetWp = False
          break   
        
        elif distanceArray[numScans/2 - i] > 5: #Checking to the right
          theta = minAngle + (numScans/2 - i - offSet)*angleIncrement
          d = distanceArray[numScans/2 - i]
          wpRel = np.array(np.cos(theta) * d, np.sin(theta) * d)
          wayPoint = (currentPos + wpRel)
          print('right')
          resetWp = False
          break
        
        
          
        
    #Move Robot
    if abs(np.linalg.norm(wayPoint - currentPos)) > .1:
      turnRobot(wayPoint)
      command.linear.x = 5.5
    else:
      command.linear.x = 0
      wayPoint = goalPos
      
        
        
    print(resetWp) 
    print 'Current Angle: {0}'.format(wayPoint)
    pub.publish(command)

# main function call
if __name__ == "__main__":
    # Initialize the node
    rospy.init_node('lab2', log_level=rospy.DEBUG)

    # subscribe to laser scan message
    sub = message_filters.Subscriber('base_scan', LaserScan)

    # subscribe to odometry message    
    sub2 = message_filters.Subscriber('odom', Odometry)

    # synchronize laser scan and odometry data
    ts = message_filters.TimeSynchronizer([sub, sub2], 10)
    ts.registerCallback(callback)

    # publish twist message
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    # Turn control over to ROS
    rospy.spin()

