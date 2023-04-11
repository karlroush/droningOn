from dronekit import connect
import sys

# Connect to the Vehicle (in this case a UDP endpoint)
vehicle = connect('127.0.0.1:14550', wait_ready=True)
print " Is Armable?: %s" % vehicle.is_armable