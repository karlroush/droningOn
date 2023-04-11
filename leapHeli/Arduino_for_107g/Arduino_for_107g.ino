// Connect anode (+) of IR LED to 5V and connect
// cathode (-) to pin 8 using a 100 ohm resistor

#define LED 8
#define STATUS 13
char val; // Data received from the serial port
int yaw;
int pitch;
int throttle;

bool loopOK;

void setup()
{
  pinMode(STATUS,OUTPUT);
  digitalWrite(STATUS,LOW);
  pinMode(LED,OUTPUT);
  digitalWrite(LED,HIGH); // turns off LED / LOW turns on
  Serial.begin(57600);
  loopOK = true;
}   

byte sendPacket(byte yaw,byte pitch,byte throttle,byte trim)
{
  static byte markL,countP,countR,one,zero;
  static bool data;
  static const byte maskB[] = {
    1,2,4,8,16,32,64,128        };
  static byte dataP[4];

  digitalWrite(STATUS,HIGH);
  dataP[0] = yaw;
  dataP[1] = pitch;
  dataP[2] = throttle;
  dataP[3] = trim;
  markL = 77;
  countP = 4;
  countR = 8;
  one = 0;
  zero = 0;
  data = true;
  while(markL--)
  {
    digitalWrite(LED,LOW);
    delayMicroseconds(10);
    digitalWrite(LED,HIGH);
    delayMicroseconds(10);
  }
  delayMicroseconds(1998);
  markL = 12;
  while(data)
  {
    while(markL--)
    {
      digitalWrite(LED,LOW);
      delayMicroseconds(10);
      digitalWrite(LED,HIGH);
      delayMicroseconds(10);
    }
    markL = 12;
    if(dataP[4-countP] & maskB[--countR])
    {
      one++;
      delayMicroseconds(688);
    }
    else
    {
      zero++;
      delayMicroseconds(288);
    }
    if(!countR)
    {
      countR = 8;
      countP--;
    }
    if(!countP)
    {
      data = false;
    }
  }
  
  while(markL--)
  {
    digitalWrite(LED,LOW);
    delayMicroseconds(10);
    digitalWrite(LED,HIGH);
    delayMicroseconds(10);
  }
  digitalWrite(STATUS,LOW);
  return((.1-.014296-one*.000688-zero*.000288)*1000); // in ms.
}

void loop()
{
  throttle = 0; //make sure the heli doesn't take off without you!
pitch =63;
  val = Serial.read(); // read it and store it in val
  while (Serial.available() > 0){
    val = Serial.read();
     if (val >= 86){
      yaw = map(val, 86, 170, 0,400);
    }
    else if (val >= 0 )
      throttle = map(val, 0, 85, 1,126);
      else if (val <=255 ) {
      pitch = map(val, 171, 255, 0,252);
    }
  }
  Serial.print(pitch);
  delay(sendPacket(yaw, pitch, throttle ,63));
}






