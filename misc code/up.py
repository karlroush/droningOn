from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil
import sys
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import msvcrt

target = 'udpin:0.0.0.0:14550'
print 'Connecting to ' + target + '...'
vehicle = connect(target, wait_ready=True)
vehicle.home_location=vehicle.location.global_frame

class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb','Index','Middle', 'Ring','Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    

    def on_init(self, controller):
        print "Loop started"

    def on_connect(self, controller):
        print "Motion Sensor Connected!"

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"
    
    def on_frame(self, controller):
        frame = controller.frame()
        previous = controller.frame(1) #The previous frame

        for hand in frame.hands:
            handType = "Left Hand" if hand.is_left else "Right Hand"
            linear_hand_movement = hand.translation(previous)
            LocationGlobalRelativeLeap=linear_hand_movement
            
            #print handType + " Hand ID:  " + str(hand.id) + " Palm Position: " + str(hand.palm_position)
            normal = hand.palm_normal
            direction = hand.direction
            '''print LocationGlobalRelativeLeap.x
            print LocationGlobalRelativeLeap.y  
            print LocationGlobalRelativeLeap.z
            print "" '''

            global x
            global y
            global z

            x= float(LocationGlobalRelativeLeap.x)
            y=float(LocationGlobalRelativeLeap.y)
            z=float(LocationGlobalRelativeLeap.z)

            return x
            return y
            return z

    def on_exit(self, controller):
        print "Loop ended" 
        print ""

def leapData():
    listener = LeapMotionListener()
    controller = Leap.Controller()  
    
    controller.add_listener(listener)
    frame=controller.frame()
    previous = controller.frame(1) #The previous frame
    hands=frame.id
    time.sleep(0.25)
    controller.remove_listener(listener)   

def send_ned_velocity(velocity_x,velocity_y,velocity_z,duration):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0,0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0,0,0,
        velocity_x,velocity_y,velocity_z,
        0,0,0,
        0,0)
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True    

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
    # time.sleep(0)

    #Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt 
        #Break and return from function just below target altitude.        
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude: 
            print "Reached target altitude"
            break
        time.sleep(1)

def flightCheck():
    print "Start Flight Check"
    vehicle = connect(connection_string, wait_ready=True)
    # Connect to the Vehicle.
    print "Connecting to vehicle on: %s" % (connection_string)
    # Get some vehicle attributes (state)
    print "Get some vehicle attribute values:"
    print " GPS: %s" % vehicle.gps_0
    print " Battery: %s" % vehicle.battery
    print " Last Heartbeat: %s" % vehicle.last_heartbeat
    print " Is Armable?: %s" % vehicle.is_armable
    print " System status: %s" % vehicle.system_status.state
    print " Mode: %s" % vehicle.mode.name    # settable
    vehicle.close()

def updateDirections():
    global xDirection
    global yDirection
    global zDirection

    if math.copysign(0.3,x)>0:
        xDirection=0.3
    elif math.copysign(0.3,x)<0:
        xDirection=-0.3
    else:
        xDirection=0

    if math.copysign(0.3,y)<0:
        yDirection=0.3
    elif math.copysign(0.3,y)>0:
        yDirection=-0.3
    else:
        yDirection=0

    if math.copysign(0.3,z)<0:
        zDirection=0.3
    elif math.copysign(0.3,z)>0:
        zDirection=-0.3
    else:
        zDirection=0
    
    return xDirection
    return yDirection
    return zDirection

def directionTS():
        print xDirection
        print yDirection 
        print zDirection



print "Starting program"
time.sleep(5)

while(True):
    #arm_and_takeoff(5)
    leapData()
    updateDirections()
    directionTS()
    send_ned_velocity(xDirection,yDirection,zDirection,2)
    if msvcrt.kbhit():
        # The user entered a key. Check to see if it was a "c".
        if (msvcrt.getch() == "q"):
            print "Activating  \"Landing\" Mode... "
            print "Landing..." 
            vehicle.mode = VehicleMode("RTL")
            #Close vehicle object before exiting script
            print "Close vehicle object"
            vehicle.close()
            break
        else:
            pass

'''
arm_and_takeoff(5) #fly to a height of 5m

North=math.copysign(0.3,LocationGlobalRelativeLeap.x)
East=math.copysign(0.3,LocationGlobalRelativeLeap.y)
Upwards=math.copysign(-0.3,LocationGlobalRelativeLeap.z)
Upwards=Upwards*-1

NORTH=0.3
WEST=-0.3
print "fly northwest"
send_ned_velocity(NORTH,WEST,0,5) # this goes 0.2 m straight if facing the coffee cabinets head on
time.sleep(1)

SOUTH=-0.3
EAST=0.3
print "fly southeast" #returns back to right above the pioneer
send_ned_velocity(SOUTH,EAST,0,5)
time.sleep(1)

upwards=-0.3
print "Fly up"
send_ned_velocity(0,0,upwards,5)
time.sleep

print "Activating  \"Landing\" Mode... "
print "Landing..." #returns to the pioneer pad, should descend
#assumes pioneer did not move and that drone returned to be directly above the landing platform
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

#40.468204, -74.444008
#40.468200, -74.443604
'''