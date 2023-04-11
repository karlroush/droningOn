from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil
import sys

target = 'udpin:0.0.0.0:14550'
print 'Connecting to ' + target + '...'
vehicle = connect(target, wait_ready=True)

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

def direction():
    print "Empty"
    #leap program here
    '''if changeX>0:
            droneXvelocity= whatever to right 1
        else:
            droneXvelocity=whatever to left -1

        if changeZ>0:
            droneZvelocity=forward 1
        else:
            droneZvelocity=back -1

        if changeY>0:
            droneYvelocity=up 1
        else:
            droneYvelocity=down -1'''
    flyCurrent(x,y,z)

def flyCurrent():
    vehicle.airspeed=3
    vehicle.velocity=3*(x,y,z)

arm_and_takeoff(2) #fly to a height of 2m

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

upwards=0.3
print "Fly up"
send_ned_velocity(0,0,upwards,5)
time.sleep

print "Activating  \"Landing\" Mode... "
print "Landing..." #returns to the pioneer pad, should descend
#assumes pioneer did not move and that drone returned to be directly above the landing platform
vehicle.mode = VehicleMode("LAND")

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

#40.468204, -74.444008
#40.468200, -74.443604