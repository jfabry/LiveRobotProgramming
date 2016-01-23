#!/usr/bin/env python
#node only to make a sub to a non-existent topic
#this is done to force a type message into a topic

import rospy
from std_msgs.msg import String


def callback(data):
    #do nothing
    return False

if __name__ == '__main__':
    try:
        rospy.init_node('bumper_sim', anonymous=True)
        rospy.Subscriber("sensors_simulator/data/destination", String, callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
