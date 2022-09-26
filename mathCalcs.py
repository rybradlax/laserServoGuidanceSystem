import Math

# when sending this data to arduino can use a char to seperate the ints so arduino knows when it's time, speed, dist, or etc
# arduino sleeps for amount of time motor is supposed to run at x speed to traverse y speed then stops rotating
class calcProperties:

    # finds min location on image (480 is bottom, 0 is top)
    def findMax(coords):
    Max = 0.0
    idx = 0
    if len(coords) > 0:
        x = 0
        for c,i in enumerate(coords):
            if int(coords[x])>Max:
                Max=coords[x]
                
                
                idx = x
            x = x + 1
    else:
        return Max,idx
    return Max,idx

    def angleProperties(pixcount):
        theta = 0.09375 * pixCount
	  theta2 = theta/11.25
	  steps = round(theta2,0)
        return theta,steps
    
    def degreesToRadians(theta):
        radians = theta * (Math.pi() / 180)
        return radians
    
    def rotationalMotionCalc(theta): # theta must be in radians
        # theta = Wo*t + (1/2)at^2, no need to account for acceleration (constant speed)
        # to travel x distance what speed and what angular distance
        # just try to make the motor move to where it needs to in 1 second and calc speed necessary for that, if it exceeds motor's max speed input max spped and find time
        # just use a set motor speed
        motorSpeed = 1.047197551196598 # rad/s
        # must convert rad/s back to arduino speed tho
        time = theta / motorSpeed
        return round(time,0) # i2c these values to arduino
        
