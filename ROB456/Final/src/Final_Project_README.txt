ROB456 Final Project Compilation

Kyle O'Brien, William Davis



1.To Run code from scratch, first get a VM running ROS-Kinetic
with Ubuntu 16.04


Instructions here:
http://wiki.ros.org/kinetic/Installation/Ubuntu



2. Make a catkin folder from home:

cd

mkdir -p ~/catkin_ws/src

catkin_make



3. Install Gmapping

sudo apt-get install ros-kinetic-slam-gmapping



4. Install move_base

sudo apt-get install ros-kinetic-navigation



5. Install explore-lite (frontier navigation for our project)

sudo apt install ros-kinetic-multirobot-map-merge ros-kinetic-explore-lite



6. Create dependencies in ~/catkin_ws folder

catkin_create_pkg rob456_project gmapping move_base roscpp rospy

catkin_create_pkg nav_bundle gmapping move_base



7. Copy/Paste my files into ~/catkin_ws/src

explore, nav_bundle, rob456_project, simpl_navigation_goals, stagebot_2dnav, CMakeLists.txt, README



8. Restart the VM. If anything up to this point is having problems, just redo the steps after restarting



9. make in ~/catkin_ws

catkin_make



10. Launching the program

#Open 3 Terminals, all at ~/catkin_ws/src folder


#Terminal 1: 

roslaunch rob456_project rob456_project.launch


#Terminal 2:

roslaunch nav_bundle nav_bundle.launch


#Terminal 3:

roslaunch explore_lite explore.launch




11. RVIZ Setup


Add -> By Topic
#Laser Scans from Robot

/base_scan LaserScan



#Frontier Waypoints

/explore /frontiers MarkerArray



#Generated Map from Scans

/map Map



#Global Costmap

/move_base /global_costmap /cost_map Map



#Local Costmap

/move_base /local_costmap /cost_map Map



#Odom (Edit parameters in RViz to make it look better)

/odom Odometry



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Program will run from here. To do improvements per map...



12. Improvements?
#In ~/catkin_ws/src/explore/launch/explore.launch

#Open with gedit or Vim, modify params to change robot's actions









