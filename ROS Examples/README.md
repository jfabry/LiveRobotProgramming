The examples in this directory are for ROS robots.

To be able to use them you should install the ROS bridge as specified in [the LRP page](http://pleiad.cl/research/software/lrp#downloads).
A separate UI will open giving the option to subcribe to topics and to allow publishing to topics.

When subscribing to a topic, a variable name should be given.
For example, you use `joint` when subscribing to `/joint_states`.
The last message recieved on that topic will be held in that variable.
In the last example, `robot joint` will give you the last message received.
Messages are objects that can be read and written in the same style as in `rospy` (but without the dots between fields as this is Smalltalk not Python :-) ).
For example, `robot joint position` will return the joint position array for the above example.

When publishing to a topic, a variable name should also be given.
For example, to move a robot that listens to the `/mobile_base/commands/velocity` topic (with messages of type Twist) you can use `velocity` as a name.
To publish to the topic, write a block to the variable.
This block will be executed once, receiving one argument: an empty message of the correct type.
The result of the block evaluation will be published on the topic, but only once.
For example, to move the previous robot forward `robot velocity: [:msg | msg linear x: 0.15]`.
Note that this message will be sent only once, so the robot will only move 1/10th of a second.
