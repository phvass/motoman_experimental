#!/usr/bin/env python
#################################################################
##\file
#
# \note
# Copyright (c) 2014 \n
# Fraunhofer Institute for Manufacturing Engineering
# and Automation (IPA) \n\n
#
#################################################################
#
# \note
# Project name: motoman_bmda3_support
# \note
# ROS stack name: motoman_experimental
# \note
# ROS package name: motoman_bmda3_support
#
# \author
# Thiago de Freitas, email:tdf@ipa.fhg.de
#
# \date Date of creation: September 2014
#
# \brief
# Some Trajectory Action for asynchronous movement on the MOTOMAN bmda3 robot
#
#################################################################
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer. \n
# - Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution. \n
# - Neither the name of the Fraunhofer Institute for Manufacturing
# Engineering and Automation (IPA) nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission. \n
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License LGPL as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License LGPL for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License LGPL along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
#################################################################


import roslib; roslib.load_manifest('motoman_bmda3_support')
import rospy
import math
import sys
import string
import actionlib
import control_msgs.msg
import trajectory_msgs.msg

from sensor_msgs.msg import JointState
from actionlib import simple_action_client
from control_msgs.msg import JointTrajectoryAction
from control_msgs.msg import FollowJointTrajectoryAction

from trajectory_msgs.msg import JointTrajectoryPoint
from std_msgs.msg import Int64

import random

class async_traj():
    def __init__(self):
        #initializing the ROS node
        rospy.init_node('async_traj_action')

        self.alternate_value = 0.0

    def async_traj_action(self):
    
        self.alternate_value = random.uniform(-1.2, 1.2)
        
        ## This generates a subscriber to the current position for the first controller
        # group. Also the joint_trajectory_action now corresponds to the trajectory
        # control for this group point_indexividually.
        msg_r1 = rospy.wait_for_message("/bmda3/bmda3_r1_controller/joint_states", JointState, 5.0)
        bmda3_r1_client = actionlib.SimpleActionClient('/bmda3/bmda3_r1_controller/joint_trajectory_action', FollowJointTrajectoryAction)
        bmda3_r1_client.wait_for_server()

        # Creates the goal object to pass to the server
        goal = control_msgs.msg.FollowJointTrajectoryGoal()

        #######################################
        # Independent trajectory for the left arm
        #######################################
        # Populates trajectory with joint names.
        goal.trajectory.joint_names = ['left_joint_1_s','left_joint_2_l','left_joint_3_e','left_joint_4_u', 'left_joint_5_r', 'left_joint_6_b', 'left_joint_7_t']

        # First trajectory point - this should always be the actual position
        # Positions
        point_index = 0
        point1 = trajectory_msgs.msg.JointTrajectoryPoint()
        point2 = trajectory_msgs.msg.JointTrajectoryPoint()
        goal.trajectory.points = [point1, point2]
        
        point1.positions = msg_r1.position
        point1.velocities = [0.0,0.0,0.0,0.0,0.0,0.0]
        point1.accelerations = [0.0,0.0,0.0,0.0,0.0,0.0]
        point1.effort = [0.0,0.0,0.0,0.0,0.0,0.0]
        goal.trajectory.points[point_index] = point1
        goal.trajectory.points[point_index].time_from_start = rospy.Duration(0.0)

        # Second trajectory point - the goal position
        # Positions
        point_index += 1
        point2.positions = [self.alternate_value,self.alternate_value,self.alternate_value,self.alternate_value,self.alternate_value,self.alternate_value]
        point2.velocities = [0.0,0.0,0.0,0.0,0.0,0.0]
        point2.accelerations = [0.0,0.0,0.0,0.0,0.0,0.0]
        point2.effort = [0.0,0.0,0.0,0.0,0.0,0.0]
        goal.trajectory.points[point_index] = point2
        goal.trajectory.points[point_index].time_from_start = rospy.Duration(2.0)
    
        goal.trajectory.header.stamp = rospy.Time.now()
        
        bmda3_r1_client.send_goal(goal)
        
        rospy.sleep(0.4)
        
        #######################################
        # Independent trajectory for the right arm
        #######################################
        
        bmda3_r2_client = actionlib.SimpleActionClient('/bmda3/bmda3_r2_controller/joint_trajectory_action', FollowJointTrajectoryAction)
        bmda3_r2_client.wait_for_server()
        msg_r2 = rospy.wait_for_message("/bmda3/bmda3_r2_controller/joint_states", JointState, 5.0)
        # Creates the goal object to pass to the server
        goal = control_msgs.msg.FollowJointTrajectoryGoal()

        # Populates trajectory with joint names.
        goal.trajectory.joint_names = ['right_joint_s_1','right_joint_2_l','right_joint_3_e','right_joint_4_u', 'right_joint_5_r', 'right_joint_6_b', 'right_joint_7_t']

        # First trajectory point
        # Positions
        point_index = 0
        #print goal.trajectory.points
        point1 = trajectory_msgs.msg.JointTrajectoryPoint()
        point2 = trajectory_msgs.msg.JointTrajectoryPoint()
        goal.trajectory.points = [point1, point2]
        
        point1.positions = msg_r2.position
        point1.velocities = [0.0,0.0,0.0,0.0,0.0,0.0]
        point1.accelerations = [0.0,0.0,0.0,0.0,0.0,0.0]
        point1.effort = [0.0,0.0,0.0,0.0,0.0,0.0]
        goal.trajectory.points[point_index] = point1
        goal.trajectory.points[point_index].time_from_start = rospy.Duration(0.0)

        # Second trajectory point
        # Positions
        point_index += 1
        point2.positions = [self.alternate_value,self.alternate_value,self.alternate_value,self.alternate_value,self.alternate_value,self.alternate_value]
        point2.velocities = [0.0,0.0,0.0,0.0,0.0,0.0]
        point2.accelerations = [0.0,0.0,0.0,0.0,0.0,0.0]
        point2.effort = [0.0,0.0,0.0,0.0,0.0,0.0]
        goal.trajectory.points[point_index] = point2
        goal.trajectory.points[point_index].time_from_start = rospy.Duration(2.0)
    
        goal.trajectory.header.stamp = rospy.Time.now()
        
        bmda3_r2_client.send_goal(goal)
        
        rospy.sleep(0.4)
        
        ###########################################
        # The following trajectories are for the both controller groups
        # that are responsible for coordinating the torso movement
        ###########################################   
        ## b1
        
        msg_b1 = rospy.wait_for_message("/bmda3/bmda3_b1_controller/joint_states", JointState, 5.0)
        msg_b2 = rospy.wait_for_message("/bmda3/bmda3_b2_controller/joint_states", JointState, 5.0)
        
        bmda3_b1_client = actionlib.SimpleActionClient('/bmda3/bmda3_b1_controller/joint_trajectory_action', FollowJointTrajectoryAction)
        bmda3_b1_client.wait_for_server()

        # Creates the goal object to pass to the server
        goal = control_msgs.msg.FollowJointTrajectoryGoal()

        # Populates trajectory with joint names.
        goal.trajectory.joint_names = ['torso_joint_b1']

        # First trajectory point
        # Positions
        point_index = 0
        #print goal.trajectory.points
        point1 = trajectory_msgs.msg.JointTrajectoryPoint()
        point2 = trajectory_msgs.msg.JointTrajectoryPoint()
        goal.trajectory.points = [point1, point2]

        point1.positions = msg_b1.position
        point1.velocities = [0.0]
        point1.accelerations = [0.0]
        point1.effort = [0.0]
        goal.trajectory.points[point_index] = point1
        goal.trajectory.points[point_index].time_from_start = rospy.Duration(0.0)

        # Second trajectory point
        # Positions
        point_index += 1
        point2.positions = [self.alternate_value]
        point2.velocities = [0.0]
        point2.accelerations = [0.0]
        point2.effort = [0.0]
        goal.trajectory.points[point_index] = point2
        goal.trajectory.points[point_index].time_from_start = rospy.Duration(2.0)
    
        goal.trajectory.header.stamp = rospy.Time.now()
        
        bmda3_b1_client.send_goal(goal)
        
        rospy.sleep(0.4)

        # B2
        bmda3_b2_client = actionlib.SimpleActionClient('/bmda3/bmda3_b2_controller/joint_trajectory_action', FollowJointTrajectoryAction)
        bmda3_b2_client.wait_for_server()

        # Creates the goal object to pass to the server
        goal = control_msgs.msg.FollowJointTrajectoryGoal()

        # Populates trajectory with joint names.
        goal.trajectory.joint_names = ['torso_joint_b2']

        # First trajectory point
        # Positions
        point_index = 0
        #print goal.trajectory.points
        point1 = trajectory_msgs.msg.JointTrajectoryPoint()
        point2 = trajectory_msgs.msg.JointTrajectoryPoint()
        goal.trajectory.points = [point1, point2]

        point1.positions = msg_b2.position
        point1.velocities = [0.0]
        point1.accelerations = [0.0]
        point1.effort = [0.0]
        goal.trajectory.points[point_index] = point1
        goal.trajectory.points[point_index].time_from_start = rospy.Duration(0.0)

        # Second trajectory point
        # Positions
        point_index += 1
        point2.positions = [self.alternate_value]
        point2.velocities = [0.0]
        point2.accelerations = [0.0]
        point2.effort = [0.0]
        goal.trajectory.points[point_index] = point2
        goal.trajectory.points[point_index].time_from_start = rospy.Duration(2.0)
    
        goal.trajectory.header.stamp = rospy.Time.now()
        
        bmda3_b2_client.send_goal(goal)
        
        rospy.sleep(2.0)

if __name__=='__main__':
    as_traj = async_traj()
    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        as_traj.async_traj_action()
        r.sleep()


