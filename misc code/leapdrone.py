# Copyright 2016 Jean-Baptiste Martin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import Leap
import argparse
import sys
import time
from dronekit import connect, VehicleMode
from argparse import RawTextHelpFormatter
from Leap import Vector

RC_MIN_VALUE = 1000  # Minimum value for a RC channel
RC_MAX_VALUE = 2000  # Maximum value for a RC channel
RC_AVG_VALUE = 1500  # Average (middle) value for a RC channel

# The Z value of palm normal (Leap Motion)
# might need to be adjusted so it is more
# intuitive to move forward
Z_VALUE_CORRECTION = 0.0

# default flight altitude (meters)
# if no command line argument is passed
DEFAULT_ALTITUDE = 5

EXIT_CODE_ERROR = 2  # exit code of application when error

# Flight mode is set to ALT_HOLD for safety measures
FLIGHT_MODE_DEFAULT = 'ALT_HOLD'

FLIGHT_MODE_LAND = 'LAND'
FLIGHT_MODE_RTL = 'RTL'
FLIGHT_MODE_GUIDED = 'GUIDED'

# Hand movement detection threshold used to detect any
# significant change in hand orientation
# this is used to avoid spamming the drone with
# non-significant changes
HAND_MOVEMENT_DETECTION_THRESHOLD = 0.1


def main():
    """
    Main function

    1. Parse ang get command line arguments
    2. Connect to vehicle
    3. Arm and take off vehicle
    4. Start leap motion movements analysis

    End of application when user hits "Enter" key.

    :return: None
    """

    global _debug  # set to True if debug argument is passed
    _debug = False

    global _rc_throttle
    _rc_throttle = 0

    altitude = DEFAULT_ALTITUDE

    # Parse arguments and options
    parser = argparse.ArgumentParser(
            description="Control a drone with your hand thanks to the Leap Motion tracker",
            formatter_class=RawTextHelpFormatter,
            epilog="NB: if both land and return to launch are set, the vehicle will only land, the priority is on land mode")
    parser.add_argument("vehicle_address",
                        help="For vehicle's address format see\n"
                             "http://python.dronekit.io/guide/connecting_vehicle.html#get-started-connecting")
    parser.add_argument("-d", "--debug", help="Show debug messages, kind of a verbose mode", action="store_true")
    parser.add_argument("-a", "--altitude",
                        metavar='Z',
                        default=DEFAULT_ALTITUDE,
                        help="Relative flight altitude in meters, default is " + str(DEFAULT_ALTITUDE) + "m",
                        type=float)
    parser.add_argument("-b", "--baud", metavar='B',
                        help="Set connection Baud rate",
                        type=int)
    parser.add_argument("-l", "--land", help="Land and disarm when flight is over", action="store_true")
    parser.add_argument("-t", "--takeoff", help="Arm and takeoff the vehicle", action="store_true", default=False)
    parser.add_argument("-o", "--overrideThrottle",
                        help="Override throttle to a value (default value is " + str(RC_AVG_VALUE) + ")",
                        metavar='VAL',
                        type=int)
    parser.add_argument("-r", "--rtl", help="Return to launch, land and disarm when flight is over",
                        action="store_true")
    args = parser.parse_args()

    vehicle_address = args.vehicle_address
    if args.debug:
        _debug = True
        print("Debug mode active")

    altitude = args.altitude

    if args.overrideThrottle:
        _rc_throttle = args.overrideThrottle

    print("Connecting to vehicle...")

    if args.baud:
        vehicle = connect(vehicle_address, wait_ready=True, baud=args.baud)
    else:
        vehicle = connect(vehicle_address, wait_ready=True)

    print("Connected")

    if args.takeoff:
        arm_and_takeoff(vehicle, altitude)

    controller = Leap.Controller()
    listener = LeapDroneListener(vehicle)
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("READY TO FLY!")
    print("Press Enter to stop...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
        if args.land or args.rtl:
            land_and_disarm(vehicle, args.land, args.rtl)

        # Remove any channels overriding
        vehicle.channels.overrides = {}
        vehicle.close()


def arm_and_takeoff(vehicle, altitude):
    """
    Arm the vehicle and take it off the ground

    When done, the vehicle's flight mode is
    switched to ALT_HOLD for easier control and
    safety

    :param vehicle: vehicle to arm and take off
    :type vehicle: dronekit.Vehicle
    :param altitude: relative altitude in meters
    :return: None
    """

    debug("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        debug(" Waiting for vehicle to initialise...")
        time.sleep(1)

    # Arming motors
    if not vehicle.armed:
        print("Arming motors")
        vehicle.armed = True
        # Confirm vehicle armed before attempting to take off
        while not vehicle.armed:
            debug(" Waiting for arming...")
            time.sleep(1)

    # Copter should arm in GUIDED mode
    debug(" Switching to GUIDED mode")
    vehicle.mode = VehicleMode(FLIGHT_MODE_GUIDED)

    # Taking off
    if vehicle.location.global_relative_frame.alt < altitude:
        print("Taking off")
        vehicle.simple_takeoff(altitude)

        while vehicle.location.global_relative_frame.alt < altitude:
            time.sleep(1)

        debug(" Vehicle reached " + str(altitude) + "m")

    # Switch flight mode to ALT_HOLD
    debug("Switching mode to " + str(FLIGHT_MODE_DEFAULT))
    vehicle.mode = VehicleMode(FLIGHT_MODE_DEFAULT)


def land_and_disarm(vehicle, land=True, rtl=False):
    """
    Land and disarm the vehicle

    The vehicle will land if the land parameter is set to True.
    If both land and rtl are set to True, the vehicle will only land.
    The priority is on landing.

    :param vehicle: vehicle to land
    :param land: land if set to True
    :param rtl: return to launch if set to True and land parameter set to false
    """
    if land or rtl:
        if land:  # priority to LAND mode
            debug("Switching mode to LAND")
            vehicle.mode = VehicleMode(FLIGHT_MODE_LAND)
        else:
            debug("Switching mode to RETURN_TO_LAUNCH")
            vehicle.mode = VehicleMode(FLIGHT_MODE_RTL)

        print("Waiting for landing and disarming...")
        while vehicle.armed:
            time.sleep(1)
        debug("Vehicle is landed and disarm")
        if land:
            vehicle.home_location = vehicle.location.global_frame


class LeapDroneListener(Leap.Listener):
    """
    Listener to be added to the Leap Motion controller
    """

    last_hand_palm_normal = None
    vehicle = None


    def __init__(self, vehicle):
        """
         :type vehicle: dronekit.Vehicle
        """
        Leap.Listener.__init__(self)
        self.vehicle = vehicle


    def on_frame(self, controller):
        """
        Function called on every frame by the
        leap motion controller

        Hand position analysis is processed here
        and vehicle rc channels are then overridden
        accordingly

        :param controller: Leap Motion controller
        :return: None
        """

        hands = controller.frame().hands

        debug("last hand palm normal: " + str(self.last_hand_palm_normal))

        # We only do something if there is one hand detected
        if len(hands) == 1:
            palm_normal = hands[0].palm_normal
            if _debug:
                debug(str(palm_normal))

            channels_override = \
                {'1': RC_AVG_VALUE - palm_normal.x * (RC_AVG_VALUE - RC_MIN_VALUE),  # RC1: Roll
                 '2': RC_AVG_VALUE - (palm_normal.z + Z_VALUE_CORRECTION) * (RC_AVG_VALUE - RC_MIN_VALUE)}  # RC2: Pitch

            if _rc_throttle:
                debug("Overriding throttle RC channel to " + str(_rc_throttle))
                channels_override['3'] = _rc_throttle  # RC3: throttle, required to be at the middle to keep altitude

            # Update the channels override only if there is
            # a significant change in the hand orientation
            if (not self.last_hand_palm_normal) \
                or not (self.vectors_equal_with_accurary(self.last_hand_palm_normal, palm_normal, HAND_MOVEMENT_DETECTION_THRESHOLD)):
                debug("Sending drone override RC channels message: " + str(channels_override))
                self.vehicle.channels.overrides = channels_override
                self.last_hand_palm_normal = palm_normal

        else:   # We disable RC 1 and 2 override to stabilize the copter
            channels_override = \
                {'1': None,
                 '2': None}
            if _rc_throttle:
                channels_override['3'] = _rc_throttle

            palm_normal = Vector()
            palm_normal.x = 0
            palm_normal.y = 0
            palm_normal.z = 0

            # Update only if changed
            if (not self.last_hand_palm_normal) \
                or not (self.vectors_equal_with_accurary(self.last_hand_palm_normal, palm_normal, HAND_MOVEMENT_DETECTION_THRESHOLD)):
                debug("Sending drone override RC channels message: " + str(channels_override))
                self.vehicle.channels.overrides = channels_override
                self.last_hand_palm_normal = palm_normal


    def vectors_equal_with_accurary(self, v1, v2, accuracy=0):
        """
        This method compares 2 vectors and return True if they are equal
        according to the accuracy passed via parameter.

        :param v1: vector 1
        :type v1: Leap.Vector
        :param v2: vector 2
        :type v2: Leap.Vector
        :param accuracy: accuracy
        :type accuracy: float
        :return: True if the vectors are equal (according to accuracy)
        """

        abs_v1_x = abs(v1.x)
        abs_v1_y = abs(v1.y)
        abs_v1_z = abs(v1.z)

        abs_v2_x = abs(v2.x)
        abs_v2_y = abs(v2.y)
        abs_v2_z = abs(v2.z)

        return  abs(abs_v1_x - abs_v2_x) <= accuracy \
            and abs(abs_v1_y - abs_v2_y) <= accuracy \
            and abs(abs_v1_z - abs_v2_z) <= accuracy



def debug(message):
    """
    Just a simple debug function to print
    a message on screen if _debug global
    variable is True

    :param message: message to print
    :return: None
    """
    global _debug
    if _debug:
        print(message)


if __name__ == '__main__':
    main()
