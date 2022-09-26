# laserServoGuidanceSystem

Main file: colorTest.py
Certain math/networking utilities were programmed for usage with a DC motor however I decided to use a servo so those utilities turned out to be unnecessary but are still programmed (mathCalcs.py, send.py, arduinoUtils.py)
(masterRPICode.py is deprecated in usage for this repository)

When running colorTest.py a user inputs 3 low and 3 high BGR values to detect an object with that range, once those values are establishes the program guides a servo with a laser and camera on it to the center position of the contour (box).

There are several different methods of doing this and that is where the AI, colorTest, and noThetaVisionAlgo come in.

The AI version of this functions identically to the colorspace files except instead of user inputted color mins and maxes it inputs a AI model that outputs boxes, the box data is analyzed in an identical manner.

The program tracks and guides the servo by incrementing its movement by 10 degrees within a certain range of pixels, then 5, then 3, then 1 until it is sufficiently close to the center of the box (using the center of the screen as the point of reference).
Whenever an angle > 180 or < 0 is reported the servo resets to 90 degrees because its range of motion is only 0-180 degrees

The altnerative way this is done is by physically calculating a theta from -90 to 90 degrees, and translating it to fit the 0-180 degree servo inputs 
This theta is calculated by creating a conversionf actor from pixels to degrees after physically measuring the amount of degrees in each individual pixel.
Note that when a DC motor is used math utilities will intake this theta and use rotational kinematics equations to solve for the required movement speed and length of time to move to most efficiently move toward the target. 
Program sleeps for a second before sending new data to arduino in an effort to not too rapidly change the data and enable smoother movement.

Data is sent to arduino to regulate laser and servo using serial library which is right now configured for the noTheta algorithm as I only measured a conversion factor for pixels to degrees in a 640 width image and do not have compatibility for any other resolutions yet so as a general use script with frames of different resolutions than (640x480) the noTheta targeting system works better
However if the resolution of the frame should be or can be 640x480 that would be the most ideal program to use (the theta targeting system)

Threaded version of this program is available but unnecessary because speeds are inherently limited by the time.sleeps placed throughout the programs.
It is recommended to not use threaded software.
