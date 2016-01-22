#!/usr/bin/env python

import roslib;
import rospy
import smach
import smach_ros
from std_msgs.msg import Bool
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction
from move_base_msgs.msg import MoveBaseGoal
from geometry_msgs.msg import Twist


destinations = {'init' : {'x': -0.68, 'y': -0.7},
    'cilinder' : {'x': -1.20, 'y': -2.23},
    'trashContainer' : {'x': 1.05, 'y': -2.24},
    'bookshelf' : {'x': 0.23, 'y': 1.02},
    'cube' : {'x': 0.42, 'y': -0.75},
    'barrier' : {'x': -3.47, 'y': 0}}

destination = 'init'

def monitor_object(ud, msg):
    return not msg.data

def monitor_bumper(ud, msg):
    return not msg.data

def monitor_destination(ud, msg):
    global destinations
    global destination
    destination = destinations[msg.data]
   
    return False

def movement_goal_cb(userdata, goal):
    global destination 

    moveGoal = MoveBaseGoal()
    moveGoal.target_pose.header.frame_id = "map"

    moveGoal.target_pose.pose.position.x = destination["x"]
    moveGoal.target_pose.pose.position.y = destination["y"]
    moveGoal.target_pose.pose.orientation.w = -1.5
    return moveGoal

def movement_origin_cb(userdata, goal):
    global destinations

    dest = destinations["init"]

    moveGoal = MoveBaseGoal()
    moveGoal.target_pose.header.frame_id = "map"

    moveGoal.target_pose.pose.position.x = dest["x"]
    moveGoal.target_pose.pose.position.y = dest["y"]
    moveGoal.target_pose.pose.orientation.w = -1.5
    return moveGoal

class Backward(smach.State):
       
    def execute(self, userdata):
        pub = rospy.Publisher('mobile_base/commands/velocity', Twist, queue_size=10)
        rate = rospy.Rate(10) # 10hz
        
        for x in range(0,5): #10 loops ~ 500 ms of moving robot backward
            twist = Twist()
            twist.linear.x = -0.2
            pub.publish(twist)
            rate.sleep()
            
        return "finish"

# main
def main():
    rospy.init_node('smach_experiment1')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['succeeded','aborted','preempted'])

    # Open the container
    with sm:


        #Creating OnOrigin machine
        sm_origin = smach.StateMachine(outcomes=['going'])
        with sm_origin:
            smach.StateMachine.add('WaitingObject', 
                                    smach_ros.MonitorState("/sensors_simulator/sensors/object", 
                                                            Bool, monitor_object),
                                    transitions={'invalid': 'WaitingDestination',
                                                'valid':'WaitingObject',
                                                'preempted': 'WaitingObject'})
            smach.StateMachine.add('WaitingDestination', 
                                    smach_ros.MonitorState("/sensors_simulator/data/destination", 
                                                            String, monitor_destination),
                                    transitions={'invalid': 'going',
                                                'valid':'WaitingDestination',
                                                'preempted': 'WaitingDestination'})
        smach.StateMachine.add('OnOrigin', sm_origin,
                                transitions={'going':'GoingToDestination'})

        #Creating OnDestination machine
        sm_destination = smach.StateMachine(outcomes=['return'])
        with sm_destination:
            smach.StateMachine.add('WaitingForRetrieving', 
                                    smach_ros.MonitorState("/sensors_simulator/sensors/bumper", 
                                                            Bool, monitor_bumper),
                                    transitions={'invalid': 'Backward',
                                                'valid':'WaitingForRetrieving',
                                                'preempted': 'WaitingForRetrieving'})
            smach.StateMachine.add('Backward', Backward(outcomes=['finish']),
                                    transitions={'finish': 'return'})
           
        smach.StateMachine.add('OnDestination', sm_destination,
                                transitions= {'return':'Returning'})
    

        # Add going and returning state to the container
        smach.StateMachine.add('GoingToDestination',
                                smach_ros.SimpleActionState('move_base',
                                                            MoveBaseAction,
                                                            goal_cb=movement_goal_cb),
                                transitions={'succeeded':'OnDestination'})
                            
        smach.StateMachine.add('Returning', 
                                smach_ros.SimpleActionState('move_base',
                                                            MoveBaseAction,
                                                            goal_cb=movement_origin_cb), 
                                transitions={'succeeded':'OnOrigin'})

    # Execute SMACH plan

    sis = smach_ros.IntrospectionServer('experiment_viz', sm, '/SM_ROOT')
    sis.start()
    
    outcome = sm.execute()
    
    rospy.spin()
    sis.stop()

if __name__ == '__main__':
    main()