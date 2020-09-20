#
# Base file to control the raspberrypi's GPIO
# python3 code
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
#num = int(t/period)
num = 1

print('Initializing GPIO...')
#print 'period =', period,'seconds'
#print 'time =', t, 'seconds'
#print 'num =', num, 'times'

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_01, GPIO.OUT) # GPIO assign mode
GPIO.setup(relay_02, GPIO.OUT) # GPIO assign mode
GPIO.setup(relay_03, GPIO.OUT) # GPIO assign mode
GPIO.setup(relay_04, GPIO.OUT) # GPIO assign mode
GPIO.setup(relay_05, GPIO.OUT) # GPIO assign mode
GPIO.setup(input_01, GPIO.IN) # GPIO assign mode
GPIO.setup(input_02, GPIO.IN) # GPIO assign mode

# Initialize GPIO outputs to HIGH (it doesn't activate the relays)
GPIO.output(relay_01, GPIO.HIGH) # output 1
GPIO.output(relay_02, GPIO.HIGH) # output 1
GPIO.output(relay_03, GPIO.HIGH) # output 1
GPIO.output(relay_04, GPIO.HIGH) # output 1
GPIO.output(relay_05, GPIO.HIGH) # output 1


print(f'Initialization, waiting {period} seconds...')
time.sleep(period)
print('done!')

try:
    # Infinite loop waiting for a CTRL^C
    while True:
        # Loop repeats num times
        for x in range(num):
            #print 'Set pin',relay_01,'(BCM) HIGH (#',x,')'
            #GPIO.output(relay_01, GPIO.HIGH)
            #time.sleep(period/60)
            print(f'Set pin {relay_01} (BCM) LOW (#{x})')
            GPIO.output(relay_01, GPIO.LOW)
            time.sleep(period)

except KeyboardInterrupt:
   GPIO.cleanup()
   print('Exiting...')

