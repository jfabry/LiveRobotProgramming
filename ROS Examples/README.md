## ROS examples ##

The examples in this directory are for ROS robots. To be able to use them you should install the ROS bridge as specified in [the LRP page](http://pleiad.cl/research/software/lrp#downloads). A separate UI will open giving the option to subscribe to topics and to allow publishing to topics.

### Subscribing to topics ###

When subscribing to a topic, a variable name should be given.
For example, you use `joint` when subscribing to `/joint_states`.
The last message received on that topic will be held in that variable.
In the last example, `robot joint` will give you the last message received.
Messages are objects that can be read and written in the same style as in `rospy` (but without the dots between fields as this is Smalltalk not Python :-) ).
For example, `robot joint position` will return the joint position array for the above example.

### Publishing to topics ###

When publishing to a topic, a variable name should also be given.
For example, to move a robot that listens to the `/mobile_base/commands/velocity` topic (with messages of type `Twist`) you can use `velocity` as a name.
To publish to the topic, write a block to the variable.
This block will be executed once, receiving one argument: an empty message of the correct type.
The result of the block evaluation will be published on the topic, but only once.
For example, to move the previous robot forward `robot velocity: [:msg | msg linear x: 0.15]`.
Note that this message will be sent only once, so the robot will only move 1/10th of a second.

### ActionLib ###

Fundamentally, Actionlib also uses publish-subscribe, and does this on a collection of topics. An overview of how this works is given in [the documentation of actionlib](http://wiki.ros.org/actionlib/DetailedDescription#Action_Interface_.26_Transport_Layer). The used topics are subtopics of the action and are as follows:

 * goal - Used to send new goals to servers
 * cancel - Used to send cancel requests to servers
 * status - Used to notify clients on the current state of every goal in the  system.
 * feedback - Used to send clients periodic auxiliary information for a goal.
 * result - Used to send clients one-time auxiliary information upon completion of a goal
 
For example, to use the navigation stack the root is typically a `/move_base` topic. Hence, to send navigation goals you should publish on the `/move_base/goal` topic, and result information is obtained from the `/move_base/result` topic. We have examples that use actionlib to do just that, for example see [the Turtlebot Transporter](https://github.com/jfabry/LiveRobotProgramming/blob/master/ROS%20Examples/Turtlebot/transporter1.lrp).
