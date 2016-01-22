#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Bool

isObject = False

def bumperNotPressed():
    global isObject
    pub = rospy.Publisher('sensors_simulator/sensors/object', Bool, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        
        if isObject:
            for x in range(0,10): #10 loops ~ 1 seconds of sending a bumper pressed message
                pub.publish(True)
                rate.sleep()
            isObject = False

        pub.publish(False)
        rate.sleep()

def pressBumper(data):
    global isObject 
    isObject = True

if __name__ == '__main__':
    try:
        rospy.init_node('bumper_sim', anonymous=True)
        rospy.Subscriber("sensors_simulator/actions/object", Empty, pressBumper)
        bumperNotPressed()
    except rospy.ROSInterruptException:
        pass
