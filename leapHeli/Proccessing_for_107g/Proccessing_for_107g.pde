/* Arduino Helicopter
 
 This code will speak to arduino through a computer's serial port
 and make a Syma 107g helicopter fly using leap!
 
 */

import processing.serial.*;
Serial myPort;
import com.onformative.leap.LeapMotionP5;
import com.leapmotion.leap.Hand;

LeapMotionP5 leap;
float xhand;
float yhand;
float zhand;
void setup()
{
  frameRate(20);
  size(500, 500, P2D);
  String portName = Serial.list()[0]; //change the 0 to a 1 or 2 etc. to match your port
  myPort = new Serial(this, "/dev/tty.usbmodem1451", 57600);
  leap = new LeapMotionP5(this);
}

void draw()
{
  background(23,23,200);
  ellipse(getHandX()+30, getHandZ()+320, 55, 55);
  
  line( 200, 500, 200, 0);
  line( 300, 500, 300, 0);
  line( 0, 200, 500, 200);
  line( 0, 300, 500, 300);

  int handCt = 0;

  for (Hand hand : leap.getHandList()) {
    if (handCt == 0)
    {
      PVector handPos = leap.getPosition(hand);
      setHandPos( handPos.x, handPos.y, handPos.z );
    }
    handCt++;

    int throttle = (int)map(getHandY(), height-100, -100, 0, 85);
    throttle = constrain(throttle, 0, 85);
    int pitch = (int)map(getHandZ(), -500, 1000, 171, 250);
    pitch = constrain(pitch, 171, 250);
    int yaw= (int)map(getHandX(), width-130, -width, 86, 170);
    yaw = constrain(yaw, 86, 170);
    myPort.write(yaw);
    myPort.write(pitch);
    myPort.write(throttle);
    println(pitch);
  }
}

void setHandPos(float x, float y, float z)
{
  xhand = x;
  yhand = y;
  zhand = z;
}

float getHandX()
{
  return xhand;
}

float getHandY()
{
  return yhand;
}
float getHandZ()
{
  return zhand;
}

