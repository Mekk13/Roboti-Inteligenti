#! /usr/bin/env python3
import math
import socket
import rospy
import time
from puppy_control.msg import Velocity
from puppy_control.msg import Pose # assuming this is the right place
from std_msgs.msg import String
from std_srvs.srv import Empty
from sensor_msgs.msg import Image
import cv2
import numpy as np

command = ''
pitch = 0
pub = None
pose_pub = None
curr_frame = None

def sparge_soseaua():
    rospy.loginfo("Spargem soseaua (Shutting down Tweety node....)")
    rospy.ServiceProxy("/puppy_control/go_home", Empty)()

def asbestos(msg):
    global curr_frame
    img_data = msg.data
    height = msg.height
    width = msg.width
    img = np.ndarray(shape=(height, width, 3), dtype=np.uint8, buffer=img_data)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    curr_frame = img
    cv2.imshow("Micunealta secreta", img)
    cv2.waitKey(1)

def sosea(msg):
    vel_msg = Velocity(x=0,y=0,yaw_rate=0)
    pose_msg = Pose(roll=math.radians(0),pitch=math.radians(0), yaw=0.000, height=-10, x_shift=-0.6, stance_x=0, stance_y=0)
    global command, pub , pitch, pose_pub
    
    local_command = msg.data
        
    if local_command == 'up':
        if local_command != command :
            vel_msg.x = 0 
            pub.publish(vel_msg)
            time.sleep(0.1)
            vel_msg.x = 20
            pub.publish(vel_msg)
        time.sleep(0.6)
    elif local_command == 'down':
        if local_command != command :
            vel_msg.x = 0 
            pub.publish(vel_msg)
            time.sleep(0.1)
            vel_msg.x = -20
            pub.publish(vel_msg)
        time.sleep(0.6)
    elif local_command == 'left':
        if local_command != command:
            vel_msg.x = 0
            vel_msg.yaw_rate = 0
            pub.publish(vel_msg)
            time.sleep(0.1)
            vel_msg.x = 7 
            vel_msg.yaw_rate = 0.4
            pub.publish(vel_msg)
        time.sleep(0.6) 
    elif local_command == 'right':
        if local_command != command:
            vel_msg.x = 0 
            vel_msg.yaw_rate = 0
            pub.publish(vel_msg)
            time.sleep(0.1)
            vel_msg.x = 7
            vel_msg.yaw_rate = -0.4
            pub.publish(vel_msg)
        time.sleep(0.6)
    elif local_command == 'look_up':
        if local_command != command:
            if pitch < 31:
                pitch += 1
                pose_msg.pitch = math.radians(pitch)
                pose_pub.publish(pose_msg)
    elif local_command == 'look_down':
        if local_command != command:
            if pitch > -31:
                pitch -= 1
                pose_msg.pitch = math.radians(pitch)
                pose_pub.publish(pose_msg)
    elif local_command == 'screenshot':
        if local_command != command:
            frame = curr_frame
            cv2.imwrite("~/images/treasure.jpg", frame)
    elif local_command == '':
        if command !=local_command :
            vel_msg.x = 0 
            vel_msg.yaw_rate = 0 
            pub.publish(vel_msg)
            time.sleep(0.1)
    command = local_command    
     
        

if __name__ == '__main__':
    rospy.init_node("TweetyNODE", log_level = rospy.DEBUG)
    rospy.on_shutdown(sparge_soseaua)

    rospy.loginfo("Hello! Tweet Tweet!")
    rospy.ServiceProxy("/puppy_control/go_home", Empty)()

    pub = rospy.Publisher("/puppy_control/velocity", Velocity, queue_size = 1)
    pose_pub = rospy.Publisher("/puppy_control/pose", Pose, queue_size = 1)

    rospy.Subscriber("Sylvester", String, sosea ,queue_size = 1)
    rospy.Subscriber("/usb_cam/image_raw", Image, asbestos , queue_size = 1)

    rospy.spin()


