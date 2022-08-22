#! /bin/env python3
import rospy
import math
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist 

received = Pose()
message = Twist()

reached_pos = reached_theta = True
x = y = angle  = 0

def callback(received):
	global angle
	global x
	global y
	angle = received.theta
	x = received.x
	y = received.y
	
def delta_theta(x_goal,y_goal,x,y):
	theta_goal =  math.atan2(y_goal-y,x_goal-x)
	return theta_goal - angle
	
def distance(x_goal,y_goal,x,y):
	return(math.sqrt((x_goal-x)**2+(y_goal-y)**2))


rospy.init_node("Locator")
rospy.Subscriber("turtle1/pose",Pose,callback)
pub = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size =10)

rate=rospy.Rate(1)

while not rospy.is_shutdown():
	if (reached_theta == True and reached_pos == True):
		x_goal = rospy.get_param("/goals/x")
		y_goal = rospy.get_param("/goals/y")
		angular_gain = rospy.get_param("/gains/angular")
		linear_gain = rospy.get_param("/gains/linear")		
		reached_theta = False
		reached_pos = False

	while (reached_theta == False):
		angleError = delta_theta(x_goal,y_goal,x,y)
		message.angular.z = angular_gain*angleError
		if (abs(angleError) < 0.000001):
			reached_theta = True
			message.angular.z = 0
		pub.publish(message)

	while (reached_pos == False):
		dis= (distance(x_goal,y_goal,x,y))
		message.linear.x = dis*linear_gain
		if(dis<0.001):
			reached_pos = True
			message.linear.x = 0
		pub.publish(message)
	
