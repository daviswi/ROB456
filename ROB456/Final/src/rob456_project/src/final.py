#!/usr/bin/env python

#import relevant libraries
import roslib
import rospy
import math

# The geometry_msgs Twist message
from geometry_msgs.msg import Twist

#the move_base result message
from move_base_msgs.msg import MoveBaseActionResult

#the probability map is full
from nav_msgs.msg import OccupancyGrid

#Width = Column = x = c
#Height = Row = y = r 

def grid_callback(msg):
  #Check if robot has reached goal
  if msg.status.status == 2 or msg.status.status == 4 or msg.status.status == 5 or msg.status.status ==6:
    print "Robot failed to reach waypoint!"
    #Recalc Frontiers
  #for index in range(0, 4000):
    #loop map
    #if map.data[index]
  
  elif msg.status.status == 3:
    print "Robot successfully reached waypoint!"
    #Move to waypoint
    


'''
  #Make a new Twist waypoint message
  waypoint = Twist()

  pub.publish(waypoint)
    
'''



def plan_callback(msg):
  #msg.data[]
  index = 5

  #for map size #SHOULD BE FOR LOCAL GRID ?TIVE?
  for x in range(0, map.info.width):
    for y in range (0, map.info.height):
      #index = location
      index = downDimension(x, y)
      #if index == -1
      if index == -1: 
        #keep in mind only record if -1 next to 99
        
    
        #check neighbors, get x/y coords
        #x = index / map.info.width
        #y = index % map.info.width
        #Check around object, x+1, y+1
        #index = 2D to 1D function(x,y)
        #if index == -1 
          #this is a frontier


  #Creates 2D Map from 1D
  #Main logic
  #x = index / map.info.width
  #y = index % map.info.width
  #print index
  x,y = upDimension(index)
  
def neighbors(x, y):
#true/false


def checkFrontier(x,y):
  if map.data[index] == -1
  for column (x-1:x+1):
    for row (y-1:y+1):
      #if neightbors(column, row) == true
      index = downDimension(column, row)
      if map.data[index] == -1
        return 

      

  #x   y-1 above
    #flag index and return true
  #x+1 y-1 top right
  #x+1 y   right
  #x+1 y+1 bot right
  #x   y+1 below
  #x-1 y+1 bot left
  #x-1 y   left 
  #x-1 y-1 top left

  #if neighbor is all -1's, return false
  #return ?true/false
  

#call with x,y and return index
def downDimension(x, y):
  #Convers 2D to 1D
  index = ((map.info.width*y) + x) 
  return index 

##call with index, return x,y location
def upDimension(index):
  #Convert 1D to 2D
  x = index / map.info.width
  y = index % map.info.width
  
  return x, y

#MAIN
if __name__ == "__main__":
  #initialize the node
  rospy.init_node('final')
  
  #publish waypoint data to root
  pub = rospy.Publisher('/base_link_goal',Twist,queue_size=10)

  #subscribe to move_base result
  sub = rospy.Subscriber('/move_base/result',MoveBaseActionResult, grid_callback)
  sub = rospy.Subscriber('map', OccupancyGrid, plan_callback)

  #turn control to ROS
  rospy.spin()


