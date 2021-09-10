import cv2
import numpy as np 
from picamera.array import PiRGBArray
from picamera import PiCamera

import RPi.GPIO as GPIO          
from time import sleep
import time
 
print("\nCode started")

GPIO.setmode(GPIO.BCM)

#Door PWM parameters
duty_cycle = 80
pwm_freq =1000

# Disk PWM parameters
disk_motor_duty_cycle = 12
disk_motor_pwm_freq = 13


# Door 1 GPIO
in1 = 20
in2 = 16
en1 = 21
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p1 = GPIO.PWM(en1,pwm_freq)
p1.start(duty_cycle)

# Door 2 GPIO
in3 = 23
in4 = 24
en2 = 25
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2 = GPIO.PWM(en2,pwm_freq)
p2.start(duty_cycle)

# Door 3 GPIO
in5 = 26
in6 = 19
en3 = 13
GPIO.setup(in5,GPIO.OUT)
GPIO.setup(in6,GPIO.OUT)
GPIO.setup(en3,GPIO.OUT)
GPIO.output(in5,GPIO.LOW)
GPIO.output(in6,GPIO.LOW)
p3 = GPIO.PWM(en3,pwm_freq)
p3.start(duty_cycle)

# Door 4 GPIO
in7 = 9
in8 = 10
en4 = 22
GPIO.setup(in7,GPIO.OUT)
GPIO.setup(in8,GPIO.OUT)
GPIO.setup(en4,GPIO.OUT)
GPIO.output(in7,GPIO.LOW)
GPIO.output(in8,GPIO.LOW)
p4 = GPIO.PWM(en4,pwm_freq)
p4.start(duty_cycle)

# Disk motor GPIO
in9 = 17
in10 = 27
en5 = 18
GPIO.setup(in9,GPIO.OUT)
GPIO.setup(in10,GPIO.OUT)
GPIO.setup(en5,GPIO.OUT)
GPIO.output(in9,GPIO.LOW)
GPIO.output(in10,GPIO.LOW)
p5 = GPIO.PWM(en5,disk_motor_pwm_freq)
p5.start(disk_motor_duty_cycle)


print("\nGPIO INIT Complete")

# Door States: open = 1, closed = 0
door1State = 0
door2State = 0
door3State = 0
door4State = 0

timeDoorIsOpened = 0
timeDoorShouldBeClosed = 0

def open_door(inA, inB):
    # forward for duration y
    GPIO.output(inA,GPIO.LOW)
    GPIO.output(inB,GPIO.HIGH)
    initialTime = int(round(time.time() * 1000))
    if inA == 20:
        openDoorAtTime = initialTime+350
        while(int(round(time.time() * 1000))< openDoorAtTime):
            pass
        #time.sleep(.350)
    else:
        openDoorAtTime = initialTime+275
        while(int(round(time.time() * 1000))< openDoorAtTime):
            pass
        #time.sleep(.275)
    # stop
    GPIO.output(inA,GPIO.LOW)
    GPIO.output(inB,GPIO.LOW)
    return
    
def close_door(inA, inB):    
    # forward for duration y
    GPIO.output(inA,GPIO.HIGH)
    GPIO.output(inB,GPIO.LOW)
    initialTime = int(round(time.time() * 1000))
    if inA == 20:
        closeDoorAtTime = initialTime+40
        while(int(round(time.time() * 1000))< closeDoorAtTime):
            pass
#         time.sleep(.040)
    if inA == 23:
        closeDoorAtTime = initialTime+50
        while(int(round(time.time() * 1000))< closeDoorAtTime):
            pass
#         time.sleep(.050)
    if inA == 26:
        closeDoorAtTime = initialTime+50
        while(int(round(time.time() * 1000))< closeDoorAtTime):
            pass
#         time.sleep(.050)
    if inA == 9:
        closeDoorAtTime = initialTime+75
        while(int(round(time.time() * 1000))< closeDoorAtTime):
            pass
#         time.sleep(.075)
    GPIO.output(inA,GPIO.LOW)
    GPIO.output(inB,GPIO.LOW)
    return

def start_disk_motor(inA, inB):
    GPIO.output(inA,GPIO.LOW)
    GPIO.output(inB,GPIO.HIGH)
    return;

def stop_disk_motor(inA, inB):
    GPIO.output(inA,GPIO.LOW)
    GPIO.output(inB,GPIO.LOW)
    return;

#Camera Initialization
camera = PiCamera()
camera.resolution = (160, 128)
while camera.analog_gain < 1:
    time.sleep(0.1)
    print('Gain:' + str(camera.analog_gain))
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode='auto'
g = camera.awb_gains
camera.awb_mode ='off'
camera.awb_gains = g
rawCapture = PiRGBArray(camera, size=(160, 128))

print("\nCamera INIT Complete")

x_blue = 3 #delta used for the H(Hue) field in HSV(Hue-Saturation-Value) for blue
x_sat_lower_blue= 90 #lower blue saturation limit for HSV
x_val_lower_blue = 100 #lower blue value limit for HSV

#Average (experimentally collected) RGB values for blue gumball as it is at the top/middle/bottom of the chute
blue_mask_top = np.uint8([[[100, 56, 26]]]) 
blue_mask_mid = np.uint8([[[87, 50, 13]]])  
blue_mask_bot = np.uint8([[[83, 60, 2]]])   

#average blue mask values in HSV format
hsvBlue_top = cv2.cvtColor(blue_mask_top,cv2.COLOR_BGR2HSV)
hsvBlue_mid = cv2.cvtColor(blue_mask_mid,cv2.COLOR_BGR2HSV)
hsvBlue_bot = cv2.cvtColor(blue_mask_bot,cv2.COLOR_BGR2HSV)

#using numpy array(byte), to hold HSV(Hue-Saturation_Value) ranges
lowerLimit_blue_top = np.uint8([hsvBlue_top[0][0][0]-x_blue,x_sat_lower_blue,x_val_lower_blue])
upperLimit_blue_top = np.uint8([hsvblue_top[0][0][0]+x_blue,255,255])
lowerLimit_blue_mid = np.uint8([hsvblue_mid[0][0][0]-x_blue,x_sat_lower_blue,x_val_lower_blue])
upperLimit_blue_mid = np.uint8([hsvblue_mid[0][0][0]+x_blue,255,255])
lowerLimit_blue_bot = np.uint8([hsvblue_bot[0][0][0]-x_blue,x_sat_lower_blue,x_val_lower_blue])
upperLimit_blue_bot = np.uint8([hsvblue_bot[0][0][0]+x_blue,255,255])


x_green = 5 #delta used for the H(Hue) field in HSV(Hue-Saturation-Value) for green
x_sat_lower_green = 90 #lower green saturation limit for HSV
x_val_lower_green = 90 #lower green value limit for HSV

#Average (experimentally collected) RGB values for green gumball as it is at the top/middle/bottom of the chute
green_mask_top = np.uint8([[[51, 116, 18]]])
green_mask_mid = np.uint8([[[54, 86, 25]]])
green_mask_bot = np.uint8([[[68, 115, 21]]])

#average green mask values in HSV format
hsvGreen_top = cv2.cvtColor(green_mask_top,cv2.COLOR_BGR2HSV)
hsvGreen_mid = cv2.cvtColor(green_mask_mid,cv2.COLOR_BGR2HSV)
hsvGreen_bot = cv2.cvtColor(green_mask_bot,cv2.COLOR_BGR2HSV)

#using numpy array(byte), to hold HSV(Hue-Saturation_Value) ranges
lowerLimit_green_top = np.uint8([hsvGreen_top[0][0][0]-x_green,x_sat_lower_green,x_val_lower_green])    
upperLimit_green_top = np.uint8([hsvGreen_top[0][0][0]+x_green,255,255])
lowerLimit_green_mid = np.uint8([hsvGreen_mid[0][0][0]-x_green,x_sat_lower_green,x_val_lower_green])
upperLimit_green_mid = np.uint8([hsvGreen_mid[0][0][0]+x_green,255,255])
lowerLimit_green_bot = np.uint8([hsvGreen_bot[0][0][0]-x_green,x_sat_lower_green,x_val_lower_green])
upperLimit_green_bot = np.uint8([hsvGreen_bot[0][0][0]+x_green,255,255])


x_yellow = 5 #delta used for the H(Hue) field in HSV(Hue-Saturation-Value) for yellow
x_sat_lower_yellow = 100 #lower yellow saturation limit for HSV
x_val_lower_yellow = 90  #lower yellow value limit for HSV

#Average (experimentally collected) RGB values for yellow gumball as it is at the top/middle/bottom of the chute
yellow_mask_top = np.uint8([[[18, 154, 162]]])
yellow_mask_mid = np.uint8([[[30, 165, 170]]]) 
yellow_mask_bot = np.uint8([[[50, 140, 140]]])

#average yellow mask values in HSV format
hsvYellow_top = cv2.cvtColor(yellow_mask_top,cv2.COLOR_BGR2HSV)
hsvYellow_mid = cv2.cvtColor(yellow_mask_mid,cv2.COLOR_BGR2HSV)
hsvYellow_bot = cv2.cvtColor(yellow_mask_bot,cv2.COLOR_BGR2HSV)

#using numpy array(byte), to hold HSV(Hue-Saturation_Value) ranges
lowerLimit_yellow_top = np.uint8([hsvYellow_top[0][0][0]-x_yellow,x_sat_lower_yellow,x_val_lower_yellow])    
upperLimit_yellow_top = np.uint8([hsvYellow_top[0][0][0]+x_yellow,255,255])
lowerLimit_yellow_mid = np.uint8([hsvYellow_mid[0][0][0]-x_yellow,x_sat_lower_yellow,x_val_lower_yellow])
upperLimit_yellow_mid = np.uint8([hsvYellow_mid[0][0][0]+x_yellow,255,255])
lowerLimit_yellow_bot = np.uint8([hsvYellow_bot[0][0][0]-x_yellow,x_sat_lower_yellow,x_val_lower_yellow])
upperLimit_yellow_bot = np.uint8([hsvYellow_bot[0][0][0]+x_yellow,255,255])


x_orange = 5 #delta used for the H(Hue) field in HSV(Hue-Saturation-Value) for orange
x_sat_lower_orange = 100 #lower orange saturation limit for HSV
x_val_lower_orange = 100 #lower orange value limit for HSV

#Average (experimentally collected) RGB values for orange gumball as it is at the top/middle/bottom of the chute
orange_mask_top = np.uint8([[[54, 108, 178]]])
orange_mask_mid = np.uint8([[[54, 99, 149 ]]])
orange_mask_bot = np.uint8([[[42, 113, 191]]])

#average orange mask values in HSV format
hsvOrange_top = cv2.cvtColor(orange_mask_top,cv2.COLOR_BGR2HSV)
hsvOrange_mid = cv2.cvtColor(orange_mask_mid,cv2.COLOR_BGR2HSV)
hsvOrange_bot = cv2.cvtColor(orange_mask_bot,cv2.COLOR_BGR2HSV)

#using numpy array(byte), to hold HSV(Hue-Saturation_Value) ranges
lowerLimit_orange_top = np.uint8([hsvOrange_top[0][0][0]-x_orange,x_sat_lower_orange,x_val_lower_orange])    
upperLimit_orange_top = np.uint8([hsvOrange_top[0][0][0]+x_orange,255,255])
lowerLimit_orange_mid = np.uint8([hsvOrange_mid[0][0][0]-x_orange,x_sat_lower_orange,x_val_lower_orange])
upperLimit_orange_mid = np.uint8([hsvOrange_mid[0][0][0]+x_orange,255,255])
lowerLimit_orange_bot = np.uint8([hsvOrange_bot[0][0][0]-x_orange,x_sat_lower_orange,x_val_lower_orange])
upperLimit_orange_bot = np.uint8([hsvOrange_bot[0][0][0]+x_orange,255,255])
 

print("\nHSV Thresholds INIT Complete")

start_disk_motor(in9, in10)
blue_gumball_counter = 0 
green_gumball_counter = 0 
yellow_gumball_counter = 0 
orange_gumball_counter = 0 


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    startTime = time.time()
    image = frame.array
    #image = cv2.GaussianBlur(image, (5,5), 0)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Blue mask mean computation
    blue_mask_top_ranging = cv2.inRange(hsv, lowerLimit_blue_top, upperLimit_blue_top)
    blue_mask_mid_ranging = cv2.inRange(hsv, lowerLimit_blue_mid, upperLimit_blue_mid)
    blue_mask_bot_ranging = cv2.inRange(hsv, lowerLimit_blue_bot, upperLimit_blue_bot)
    blue_mask_temp = cv2.bitwise_or(blue_mask_top_ranging, blue_mask_mid_ranging)
    blue_mask = cv2.bitwise_or(blue_mask_temp, blue_mask_bot_ranging)
    blue_mask_mean = cv2.mean(blue_mask)[0]
    #print("Blue mask: " + str(blue_mask_mean))
 
    # Green mask mean computation
    green_mask_top_ranging = cv2.inRange(hsv, lowerLimit_green_top, upperLimit_green_top)
    green_mask_mid_ranging = cv2.inRange(hsv, lowerLimit_green_mid, upperLimit_green_mid)
    green_mask_bot_ranging = cv2.inRange(hsv, lowerLimit_green_bot, upperLimit_green_bot)
    green_mask_temp = cv2.bitwise_or(green_mask_top_ranging, green_mask_mid_ranging)
    green_mask = cv2.bitwise_or(green_mask_temp, green_mask_bot_ranging)
    green_mask_mean = cv2.mean(green_mask)[0]
    #print("Green mask: " + str(green_mask_mean))
        
    # Yellow mask mean computation
    yellow_mask_top_ranging = cv2.inRange(hsv, lowerLimit_yellow_top, upperLimit_yellow_top)
    yellow_mask_mid_ranging = cv2.inRange(hsv, lowerLimit_yellow_mid, upperLimit_yellow_mid)
    yellow_mask_bot_ranging = cv2.inRange(hsv, lowerLimit_yellow_bot, upperLimit_yellow_bot)
    yellow_mask_temp = cv2.bitwise_or(yellow_mask_top_ranging, yellow_mask_mid_ranging)
    yellow_mask = cv2.bitwise_or(yellow_mask_temp, yellow_mask_bot_ranging)
    yellow_mask_mean = cv2.mean(yellow_mask)[0]
    #print("Yellow mask: " + str(yellow_mask_mean))
    
    # Orange mask mean computation
    orange_mask_top_ranging = cv2.inRange(hsv, lowerLimit_orange_top, upperLimit_orange_top)
    orange_mask_mid_ranging = cv2.inRange(hsv, lowerLimit_orange_mid, upperLimit_orange_mid)
    orange_mask_bot_ranging = cv2.inRange(hsv, lowerLimit_orange_bot, upperLimit_orange_bot)
    orange_mask_temp = cv2.bitwise_or(orange_mask_top_ranging, orange_mask_mid_ranging)
    orange_mask = cv2.bitwise_or(orange_mask_temp, orange_mask_bot_ranging)
    orange_mask_mean = cv2.mean(orange_mask)[0]
    #print("Orange mask: " + str(orange_mask_mean))
    


    #result = cv2.bitwise_and(image,image, mask = cv2.bitwise_or(cv2.bitwise_or(blue_mask,green_mask), cv2.bitwise_or(yellow_mask,orange_mask)))
    cv2.imshow("Frame", image)
    #cv2.imshow("Blue Mask", blue_mask)
    #cv2.imshow("Green Mask", green_mask)
    #cv2.imshow("Yellow Mask", yellow_mask)
    #cv2.imshow("Orange Mask", orange_mask)
    #cv2.imshow("Red Mask", red_mask)
    #cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
    #cv2.imshow("Result", result)
    
    if (blue_mask_mean > 0.75) & (door1State==0): #If blue is detected and the corresponding door is closed
        #print("Blue mask: " + str(blue_mask_mean))
        blue_gumball_counter += 1
        #print(str(blue_gumball_counter))
        print("blue")
        timeDoorIsOpened = int(round(time.time() * 1000))
        timeDoorShouldBeClosed = timeDoorIsOpened+1100
        open_door(in1, in2)
        door1State = 1
      
    if (green_mask_mean > 0.75) & (door2State==0): #If green is detected and the corresponding door is closed
        #print("Green mask: " + str(green_mask_mean))
        green_gumball_counter += 1
        #print(str(green_gumball_counter))
        print("green")
        timeDoorIsOpened = int(round(time.time() * 1000))
        timeDoorShouldBeClosed = timeDoorIsOpened+900
        open_door(in3, in4)
        door2State = 1
        
    if (yellow_mask_mean > 1) & (door3State == 0): #If yellow is detected and the corresponding door is closed
        print("Yellow mask: " + str(yellow_mask_mean))
        yellow_gumball_counter += 1
        #print(str(yellow_gumball_counter))
        print("yellow")
        timeDoorIsOpened = int(round(time.time() * 1000))
        timeDoorShouldBeClosed = timeDoorIsOpened+750
        open_door(in5, in6)
        door3State = 1
        
    if (orange_mask_mean > 0.75) & (orange_mask_mean < 4) & (door4State == 0): #If orange is detected and the corresponding door is closed
        print("Orange mask: " + str(orange_mask_mean))
        orange_gumball_counter += 1
        #print(str(orange_gumball_counter))
        print("orange")
        timeDoorIsOpened = int(round(time.time() * 1000))
        timeDoorShouldBeClosed = timeDoorIsOpened+750
        open_door(in7, in8)
        door4State = 1
    
    if (int(round(time.time() * 1000))>=timeDoorShouldBeClosed):
        if door1State == 1:
            close_door(in1,in2)
            door1State = 0
            
        if door2State == 1:
            close_door(in3,in4)
            door2State = 0
            
        if door3State == 1:
            close_door(in5,in6)
            door3State = 0
        
        if door4State == 1:
            close_door(in7,in8)
            door4State = 0

    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key == 27:
            break
        
    TotalTime = time.time()
    print('Total Processing Time: '+str(TotalTime-startTime))


stop_disk_motor(in9, in10)
cv2.destroyAllWindows()
GPIO.cleanup()

#Printing counters for each color:
print("# blue: " + str(blue_gumball_counter))
print("# green: " + str(green_gumball_counter))
print("# yellow: " + str(yellow_gumball_counter))
print("# orange: " + str(orange_gumball_counter))
