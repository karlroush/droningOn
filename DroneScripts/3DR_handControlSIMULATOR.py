from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil
import sys
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import msvcrt
import statistics

#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', 
                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

target = args.connect
sitl = None

#Start SITL if no connection string specified
if not target:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    target = sitl.connection_string()

#target = 'udpin:0.0.0.0:14550'
print 'Connecting to ' + target + '...'
vehicle = connect(target, wait_ready=True)
#vehicle.home_location=vehicle.location.global_frame

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
            print LocationGlobalRelativeLeap.x
            print LocationGlobalRelativeLeap.y  
            print LocationGlobalRelativeLeap.z
            print "" 

            global x
            global y
            global z

            x=float(LocationGlobalRelativeLeap.x)
            xData.append(x)
            z=float(LocationGlobalRelativeLeap.y)
            zData.append(z)
            y=float(LocationGlobalRelativeLeap.z)
            yData.append(y)

            x=statistics.median(xData)
            y=statistics.median(yData)
            z=statistics.median(zData)

            if abs(x)>abs(y) and abs(x)>abs(z):
                x=x
                y=0
                z=0
            elif abs(y)>abs(x) and abs(y)>abs(z):
                y=y
                x=0
                z=0
            elif abs(z)>abs(x) and abs(z)>abs(y):
                z=z
                x=0
                y=0
            else:
                x=0
                y=0
                z=0

            return x
            return y
            return z
            print x, y, z

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

def send_ned_velocity(velocity_x,velocity_y,velocity_z):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0,0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0,0,0,
        velocity_x,velocity_y,velocity_z,
        0,0,0,
        0,0)
    dur=0
    while dur<0.25:
        vehicle.send_mavlink(msg)
        time.sleep(0.05)
        dur=dur+0.05

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
    # Connect to the Vehicle.
    print "Connecting to vehicle on: %s" % (target)
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

    if x==0:
        xDirection=0
    elif math.copysign(0.3,x)>0:
        xDirection=0.5
    elif math.copysign(0.3,x)<0:
        xDirection=-0.5
    else:
        xDirection=0

    if y==0:
        yDirection=0
    elif math.copysign(0.3,y)<0:
        yDirection=0.5
    elif math.copysign(0.3,y)>0:
        yDirection=-0.5
    else:
        yDirection=0
    
    if z==0:
        zDirection=0
    elif math.copysign(0.3,z)<0:
        zDirection=0.5
    elif math.copysign(0.3,z)>0:
        zDirection=-0.5
    else:
        zDirection=0
    
    return xDirection
    return yDirection
    return zDirection

def directionTS():
        print "X velocity:", xDirection
        print "Y velocity:", yDirection 
        print "Z velocity:", zDirection

def upAndDown():
    arm_and_takeoff(5)
    print "Activating  \"Landing\" Mode... "
    print "Landing..." 
    vehicle.mode = VehicleMode("RTL")
    #Close vehicle object before exiting script
    print "Close vehicle object"
    vehicle.close()


print "Starting program"
time.sleep(2)

global x
global y
global z
x=0.1
y=0.1
z=0.1

global xData
global yData
global zData
xData=[]
yData=[]
zData=[]

arm_and_takeoff(7)
time.sleep(2)
print "Hand control enabled"

while(True):
    leapData()
    xData=[]
    yData=[]
    zData=[]
    updateDirections()
    directionTS()
    send_ned_velocity(xDirection,yDirection,zDirection)
    time.sleep(1)
    if msvcrt.kbhit():
        # The user entered a key. Check to see if it was a "q".
        if (msvcrt.getch() == "q"):
            print "Activating  \"Landing\" Mode... "
            print "Landing..." 
            vehicle.mode = VehicleMode("RTL")
            #Close vehicle object before exiting script
            print "Close vehicle object"
            vehicle.close()
            if sitl is not None:
                sitl.stop()
            break
        else:
            pass