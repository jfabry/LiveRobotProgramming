#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def showAndAction(data):
    toSend = raw_input(data.data+"\n")
    pub = rospy.Publisher('lrp/input_data', String, queue_size=10)
    pub.publish(toSend)
    
def showText(data):
    print data.data+"\n"

if __name__ == '__main__':
    rospy.init_node('lrp_interface', anonymous=True)
    pub = rospy.Publisher('lrp/input_data', String, queue_size=10)
    pub.publish("init")
 
    rospy.Subscriber("lrp/input_text", String, showAndAction)
    rospy.Subscriber("lrp/show_text", String, showText)
    rospy.spin()
    
