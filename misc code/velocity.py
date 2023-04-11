#d code
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil
import sys


#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', 
                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


###Start SITL if no connection string specified
##if not connection_string:
##    import dronekit_sitl
##    sitl = dronekit_sitl.start_default()
##    connection_string = sitl.connection_string()

target = sys.argv[1] if len(sys.argv) >= 2 else 'udpin:0.0.0.0:14550'
print 'Connecting to ' + target + '...'
vehicle = connect(target, wait_ready=True)
# Connect to the Vehicle
#print 'Connecting to vehicle on: %s' % connection_string
#vehicle = connect(connection_string, wait_ready=True)

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
        # time.sleep(0)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
    # time.sleep(0)

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt 
        #Break and return from function just below target altitude.        
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude: 
            print "Reached target altitude"
            break
        time.sleep(1)

arm_and_takeoff(2) #1 meter from ground to table, 1.1 if account for legs and 1.2 for reaching over cup
#if vehicle.location.global_relative_frame.alt < 2:
#    arm_and_takeoff(2) 
NORTH=0.2732050808
WEST=-0.2
print "fly northwest"
send_ned_velocity(NORTH,WEST,0,5) # this goes 0.2 m straight if facing the coffee cabinets head on
time.sleep(1)

SOUTH=-0.2732050808
EAST=0.2
print "fly southeast" #returns back to right above the pioneer
send_ned_velocity(SOUTH,EAST,0,5)
time.sleep(1)


##print "Set default/target airspeed to 3"
##vehicle.airspeed = 3
##
##print "Going towards first point for 30 seconds ..."
##point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
##vehicle.simple_goto(point1)
##
### sleep so we can see the change in map
##time.sleep(30)
##
##print "Going towards second point for 30 seconds (groundspeed set to 10 m/s) ..."
##point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
##vehicle.simple_goto(point2, groundspeed=10)
##
### sleep so we can see the change in map
##time.sleep(30)

#send_ned_velocity(0,0,0.2,5)
print "Activating  \"Landing\" Mode... "
print "Landing..." #returns to the pioneer pad, should descend
#assumes pioneer did not move and that drone returned to be directly above the landing platform
vehicle.mode = VehicleMode("LAND")

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()
