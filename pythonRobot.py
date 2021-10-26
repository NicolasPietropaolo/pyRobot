'''
 
Program controls Raspberry Pi 3 Robot

Uses PWM

'''

#Import Libraries

import RPi.GPIO as GPIO
import time

#Set up GPIO mode 

GPIO.setmode(GPIO.BCM) # BCM Pin references are being used
GPIO.setwarnings(False)

#Set up GPIO pins

motASpeed = 12
motADir = 5
motBSpeed = 13
motBDir = 6
trigger = 16
echo = 19


#Set pin modes - use variables from previous section

GPIO.setup(motASpeed,GPIO.OUT)
GPIO.setup(motADir,GPIO.OUT)
GPIO.setup(motBSpeed,GPIO.OUT)
GPIO.setup(motBDir,GPIO.OUT)
GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)


#implement PWM for the motors

freq = 50
pwmMotA = GPIO.PWM(motASpeed,freq)
pwmMotB = GPIO.PWM(motBSpeed,freq)


# Motor Functions
def stop():     #To stop the robot 
    #Turns motors off stopping  robot
    pwmMotA.ChangeDutyCycle(0)
    pwmMotB.ChangeDutyCycle(0)

def forward(A,B):       #For moving robot forwards
    #Causes robot to drive forward in a straight line
    pwmMotA.ChangeDutyCycle(A)
    GPIO.output(motADir,1)
    pwmMotB.ChangeDutyCycle(B)
    GPIO.output(motBDir,1)
    
def backward(A,B):      #For moving robot backwards
    #Causes the robot to drive backward in a straight line
    
    pwmMotA.ChangeDutyCycle(A)
    GPIO.output(motADir,0)
    pwmMotB.ChangeDutyCycle(B)
    GPIO.output(motBDir,0)
    
def right(A,B):     #For moving robot right
    #Causes the robot to keep turning to the right
    
    pwmMotA.ChangeDutyCycle(A)
    GPIO.output(motADir,0)
    pwmMotB.ChangeDutyCycle(B)
    GPIO.output(motBDir,1)
def left(A,B):      #For moving robot left
    #Causes the robot to keep turning to the left
    pwmMotA.ChangeDutyCycle(A)
    GPIO.output(motADir,1)
    pwmMotB.ChangeDutyCycle(B)
    GPIO.output(motBDir,0)
    
# Obstacle Avoidance 
def checkDistance():
    #Uses ultrasonic sensor to check how far away objects are from the front of the robot
    
    # Set up GPIO outputs to shoot an ultrasonic pulse

    GPIO.output(trigger,False)      # Turn sonic trigger off
    time.sleep(0.5)                  # Let module settle for 0.5 second
    GPIO.output(trigger,True)          # Turn sonic trigger on to emit a pulse
    time.sleep(0.00001)                  # Sleep for 10 microseconds to send out a 10 microsecond pulse
    GPIO.output(trigger,False)      # sonic trigger off

    startTime = time.time()               # Records start time
    while GPIO.input(echo)== False:     # Check if the echo pin has not received a pulse yet 
        startTime = time.time()            # Update start time with current time

    while GPIO.input(echo)==True:     # Check if echo pin has received a pulse
        stopTime = time.time()             # Keep track of when the pulse returned

        
        if stopTime - startTime >= 0.04:     # Checks if elapsed time is >0.04 seconds - object is likely too close
            print("Hold it! You're too close for me to see.")
            stopTime = startTime         # Set stop time to start time
            break

    totTime = time.time()-startTime                  # Calculate total elapsed time from start to finish

    distance = 34326*totTime/2                 # Calculate distance of the detected object

    
    return distance #returns calculated distance 


def isNearObstacle(howNear):
    distance = checkDistance()                # Find distance of object using previously made function 
    print("isNearObstacle: " + str(distance))

    if howNear > distance:                 # Check if obstacle is too close
        return True
    else:
        return False

def avoidObstacle(reverseTime, turnTime):
    # Back off a little
    print("Backwards")
    backward(70,70)                # experiment with backward() to find good A and B values
    time.sleep(reverseTime)                # Reverse for a certain amount of time (s)   
    stop()

    # Turn right
    print("Right")
    right(70,70)                   # experiment with right() first to find good A and B values
    # Experiment to find time that causes for a 90 degree turn 
    time.sleep(turnTime)
    stop()
    
# Start motors 

pwmMotA.start(0)
pwmMotB.start(0)

# experiment to find the right turnTime for a 90 degree turn
howNear = 15                        #distance (cm) an object must be for the robot to reverse and turn right      
reverseTime= 1                   #the time (s) that  robot will reverse for
turnTime = 1                  #the time (s) that the robot will turn right for

### try-except allows robot to drive around and avoid obstacles until user presses CTRL+C
try:
    
    GPIO.output(trigger,False)  # Set trigger to False (Low)

    
    time.sleep(0.1) # Allow module to settle

    # next loop repeated infinitely
    while True:
        forward(50, 50)             #Found A and B values needed to make the robot go in a straight line
        time.sleep(0.01)             # Slight pause to let module settle
        if isNearObstacle(howNear):  # Checks if you are close to an obstacle and stops robot
            stop() 
           
            avoidObstacle(reverseTime,turnTime) # Avoid Obstacles robot completes a 90 degree turn 

### CTRL+C, cleanup and stop 
except KeyboardInterrupt:
    GPIO.cleanup()

