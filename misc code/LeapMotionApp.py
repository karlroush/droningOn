import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.Listener):
	finger_names=['Thumb','Index','Middle','Ring', 'Pinky']
	bone_names=['Metacarpal','Proximal','Intermediate','Distal']
	state_names=['STATE_INVALID','STATE_START','STATE_UPDATE','STATE_END']

	def on_init(self, controller):
		print "Intialized"

	def on_connect(self, controller):
		print "Motion sensor connected"

		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		print "Motion sensor disconnected"

	def on_exit(self,controller):
		print "Exited"

	def on_frame(self,controller):
		pass

def main():
	listener= LeapMotionListener()
	controller=Leap.Controller()

	controller.add_listener(listener)

	print "Press enter to quit"
	try:
		pass
	except KeyboardInterrupt:
		pass
	finally:
		#controller.remove_listner(listener)
		pass

if __name__=="__main__":
	main()