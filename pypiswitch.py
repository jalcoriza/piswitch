#
# Base file to control the raspberrypi's GPIO
# python2 code
#
import RPi.GPIO as GPIO
import time

relay_01 = 4 # BCM4, pin7, OUT-01, bulb light
relay_02 = 17 # BCM17, pin11, OUT-02, garage door
relay_03 = 27 # BCM27, pin13, OUT-03
relay_04 = 22 # BCM22, pin15, OUT-04
relay_05 = 10 # BCM10, pin19, OUT-05
input_01 = 9 # BCM9, pin21, IN-01, short input
input_02 = 11 # BCM11, pin23, IN-02, long input

#period = 0.01 # Period in seconds
period = 60 # Period in seconds
t = 3600 * 24 # Time in seconds
num = int(t/period)

print('Initializing GPIO...')
print 'period =', period,'seconds'
print 'time =', t, 'seconds'
print 'num =', num, 'times'

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_01, GPIO.OUT) # GPIO assign mode
GPIO.setup(relay_02, GPIO.OUT) # GPIO assign mode
GPIO.setup(relay_03, GPIO.OUT) # GPIO assign mode
GPIO.setup(relay_04, GPIO.OUT) # GPIO assign mode
GPIO.setup(relay_05, GPIO.OUT) # GPIO assign mode
GPIO.setup(input_01, GPIO.IN) # GPIO assign mode
GPIO.setup(input_02, GPIO.IN) # GPIO assign mode

#GPIO.output(relay_01, GPIO.LOW) # output 0

try:
    # Infinite loop waiting for a CTRL^C
    while True:
        # num Loop
        for x in range(num):
            print 'Set pin',relay_01,'(BCM) HIGH (#',x,')'
            GPIO.output(relay_01, GPIO.HIGH)
            time.sleep(period/60)
            print 'Set pin',relay_01,'(BCM) LOW (#',x,')'
            GPIO.output(relay_01, GPIO.LOW)
            time.sleep(period)

except KeyboardInterrupt:
   GPIO.cleanup()
   print('Exiting...')

