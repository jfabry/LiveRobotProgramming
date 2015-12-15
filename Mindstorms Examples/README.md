The examples in this directory are for the Lego Mindstorms EV3.

To be able to use them you should install the EV3 bridge as specified in [the LRP page](http://pleiad.cl/research/software/lrp#downloads).
When the network connection is set up, a UI will appear that allows you to inspect the different objects that represent the different sensors and motors.
From within LRP action blocks (i.e. Smalltalk code) `robot sensor1` to `robot sensor4` will give you the different sensor objects and `robot motorA` to `robot motorD` the different motors.

To get sensor values, send the message `read` to a sensor.
To have the motor operate there are multiple possible ways.
The most straightforward is something like `robot motorA startAtSpeed: 50` and `robot motorA stop`.
We advise you to browse the motor classes and examine the examples there.

