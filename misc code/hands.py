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
			count=0
			LocationGlobalRelativeLeap.x=LocationGlobalRelativeLeap.x/1000000
			LocationGlobalRelativeLeap.y=LocationGlobalRelativeLeap.y/1000000
			LocationGlobalRelativeLeap.z=LocationGlobalRelativeLeap.z/10
			
			print""
			print"Hand Palm Position [X,Y,Z]"
			print hand.palm_position[0]
			print hand.palm_position[1]
			print hand.palm_position[2]
			print ""
			print "Palm Position Change [X,Y,Z]"
			print LocationGlobalRelativeLeap.x
			print LocationGlobalRelativeLeap.y
			print LocationGlobalRelativeLeap.z
			if LocationGlobalRelativeLeap.x>0:
				print 'droneXvelocity= whatever to right'
			else:
				print 'droneXvelocity=whatever to left'
			if LocationGlobalRelativeLeap.y>0:
				print 'droneYvelocity=up'
			else:
				print 'droneYvelocity=down'
			if LocationGlobalRelativeLeap.z>0:
				print 'droneZvelocity=forward'
			else:
				print 'droneZvelocity=back'

			return LocationGlobalRelativeLeap.x
			return LocationGlobalRelativeLeap.y			
			return LocationGlobalRelativeLeap.z
			
	def on_exit(self, controller):
		print "Exited"  

def new():
	listener = LeapMotionListener()
	controller = Leap.Controller()	
	
	controller.add_listener(listener)
	frame=controller.frame()
	previous = controller.frame(1) #The previous frame
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
	new()