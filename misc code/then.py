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
			
			#print handType + " Hand ID:  " + str(hand.id) + " Palm Position: " + str(hand.palm_position)
			normal = hand.palm_normal
			direction = hand.direction
			count=0
			
			print""
			print"hand palm Position [X,Y,Z]"
			print hand.palm_position[0]
			print hand.palm_position[1]
			print hand.palm_position[2]
			print linear_hand_movement
			print linear_hand_movement * 10
			
	def on_exit(self, controller):
		print "Exited"  

def main():
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
	main()