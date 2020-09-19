# Quick & dirty code to turn on the light
# python2
import RPi.GPIO as GPIO
import time

relay_01 = 4 # BCM4, pin7
relay_02 = 17 # BCM17, pin11
relay_03 = 27 # BCM27, pin13
relay_04 = 22 # BCM22, pin15
relay_05 = 10 # BCM10, pin19
input_01 = 9 # BCM9, pin21
input_02 = 11 # BCM11, pin23

#period = 0.01 # Period in seconds
period = 10 # Period in seconds
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
    print 'Set pin',relay_01,'(BCM) LOW '
    GPIO.output(relay_01, GPIO.LOW)
    time.sleep(period)

    GPIO.cleanup()
    print('Exiting...')

except KeyboardInterrupt:
    GPIO.cleanup()
    print('Exiting...')

