WINLAB Summer 2016
Gesture Based Drone Control
droningOn: Alissa Tsai, Fred Tang, Karl Roush

Objective: Create a control system for a 3DR solo drone that utilizes the user’s hand movements to influence the flight of the drone, all while making the project easy to modify and readily accessible.

TO RUN THE PROGRAM (GestureControl_finalRelease.py):
1) Follow the necessary steps to connect your vehicle. If the connection string for your vehicle is not udpin:0.0.0.0:14550 , be sure to change it on line 27 of the program. 
      3DR Drone specific steps:
          1) Turn both the controller and drone on.
          2) Wait for the controller to aquire a GPS fix.
          3) Connect to the controller like how you would for any other wifi network. The default password is "sololink".
          4) If you wish to connect both the vehicle and computer to the internet, type:  "solo wifi --name=<n> --password=<p>". Then reconnect to the controller once it has finished.
          5) Run the command "solo info" to insure that you are connected. If you are not connected, repeat steps 1-3 (4 if applicable).
          Further help can be found at: https://dev.3dr.com/starting-utils.html
2) Open command prompt or equivalent application on your computer.
3) Navigate to the directory containing "GestureControl_finalRelease.py" .
4) Modify any items in the program (as needed) using any code editor. Be sure to save it when you are done making changes.
5) Run the program by typing "python GestureControl_finalRelease.py"
6) After the vechile reaches the specified targert altitude, the program will notify you that it has done so with the text "Reached target altitude". At this point, you have 2 seconds to place you hand over the Leap Motion device.
7) The program will display "Hand control enabled" at this point and you are free to begin controlling the drone.
      IMPORTANT: The Leap Motion by default samples a space of 0.25 seconds at intervals 1 second. Any motion not within the sample space will not be taken into account. To modidy this, see "Configuration Notes".

TO EXIT THE PROGRAM:
1) Press "q" on your keyboard or the esc key.
2) The program will display "Activating  'Landing' Mode... " then "Landing..." .
3) The vehicle will return to its initial location, then land and turn off.

CONFIGURATION NOTES:
Connection string- Can be changed on line 27 by modifying the "target" variable. Default is udpin:0.0.0.0:14550 which is for the 3DR Solo Drone connection over wifi
Duration of Leap Motion data collection- Change the value of time.sleep(0.25) on line 113. Default is 0.25 seconds. IMPORTANT! The variable dur (line 126)  must be changed to match this. This is to prevent a mismatch between the Leap Motion data and the flight data commands sent to the drone. It is possible to not have them match, though that would require additional configuration by the user and should not be attempted unless they are certain it will not interfere with other components.
Initial takeoff height- Change the parameter of arm_and_takeoff(7) on line 249. The default height is 7 meters.
Program end keys- Change the value of "q" to which ever key you desire on line 264 (if (msvcrt.getch() == "q").

ADDITIONAL FEATURES:
Running the program on a simulator- 
      Runs the program on a SITL Simulator. 
      Un-comment lines 12-26, Comment out lines 27 and 30, alternatively run "3DR_handControlSIMULATOR.py" under droningOn>DroneScripts.
Performing a Flight Check-
      Brings up information about the vehicle such as connection string, GPS location, battery percent, status, if it is armable, and more.
      Type “flightCheck()” onto line 248.
Simple Takeoff and Land-
      Vehicle takes off and flies to a specified altitude (default= 5 meters), then comes back and lands.
      Type “upAndDown()” onto line 248.
      Altitude can be changed via the parameter in arm_and_takeoff() on line 223
      
Special thanks to Professors Ivan Seskar & Wade Trappe, as well as Rutgers University and Rutgers Wireless Information Network Lab

