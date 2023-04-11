import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
	
class LeapMotionListener(Leap.Listener):
	finger_names = ['Thumb','Index','Middle', 'Ring','Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

	def on_init(self, controller):
		print "Initialized"

	def on_connect(self, controller):
		print "Motion Sensor Connected!"

		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		print "Motion Sensor Disconnected"

	def on_exit(self, controller):
		print "Exited"  
	'''def on_frame(self, controller):
		frame = controller.frame()
		print "Frame ID:  " + str(frame.id) \
			= "Timestamp:  " + str(frame.timestamp) \
			= "# of Hands  " + str(len(frame.hands)) \
			= "# of Fingers  " + str(len(frame.fingers)) \
			= "# of Tools  " + str(len(frame.tools)) \
			= "# of Gestures  " + str(len(frame.gestures)) \''''
	'''def leap_to_world(self, leap_point, iBox):
		hand_center = hand.palm_position
	    print hand_center
	    leap_point.z *= -1.0; #right-hand to left-hand rule
	    normalized = iBox.normalize_point(leap_point, False)
	    normalized = normalized + Leap.Vector(0.5, 0, 0.5); #recenter origin
	    return normalized * 100.0; #scale'''
	def on_frame(self, controller):
		frame = controller.frame()

		for hand in frame.hands:
			handType = "Left Hand" if hand.is_left else "Right Hand"
			
			#print handType + " Hand ID:  " + str(hand.id) + " Palm Position: " + str(hand.palm_position)
			normal = hand.palm_normal
			direction = hand.direction
			count=0
			print""
			print"hand palm Position [X,Y,Z]"
			print hand.palm_position[0]
			print hand.palm_position[1]
			print hand.palm_position[2]

		def go_to(): #this is for moving the drone based off of the direct coordinates from the Leap
			# Set mode to guided - this is optional as the goto method will change the mode if needed.
			vehicle.mode = VehicleMode("GUIDED")
			x=hand.palm_position[0]
			y=hand.palm_position[1]
			z=hand.palm_position[3]
			# Set the target location in global-relative frame
			a_location = LocationGlobalRelative(x, y, z)
			vehicle.simple_goto(a_location)

def main():
	listener = LeapMotionListener()
	controller = Leap.Controller()	
	
	controller.add_listener(listener)
	frame=controller.frame()
	hands=frame.id
	#first_hand=hands()
	#hand.center=hand.palm_position
	#print hand_center
	
	print "Press enter to quit"
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)

if __name__ == "__main__":
	main()