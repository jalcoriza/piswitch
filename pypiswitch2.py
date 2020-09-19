# Quick & dirty code to test garage door
# python2
import RPi.GPIO as GPIO
import time

relay_01 = 4 # BCM4, pin7
relay_02 = 17 # BCM17, pin11

#period = 0.01 # Period in seconds
period = 2 # Period in seconds
t = 3600 * 24 # Time in seconds
num = int(t/period)

print('Initializing GPIO...')
print 'period =', period,'seconds'
print 'time =', t, 'seconds'
print 'num =', num, 'times'

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_01, GPIO.OUT) # GPIO assign mode
GPIO.setup(relay_02, GPIO.OUT) # GPIO assign mode

GPIO.output(relay_01, GPIO.HIGH) # output 1
GPIO.output(relay_02, GPIO.HIGH) # output 1

try:
    for x in range(1):
        print 'Set pin',relay_02,'(BCM) HIGH (#',x,')'
        GPIO.output(relay_02, GPIO.HIGH)
        time.sleep(period)
        print 'Set pin',relay_02,'(BCM) LOW (#',x,')'
        GPIO.output(relay_02, GPIO.LOW)
        time.sleep(period)
        print 'Set pin',relay_02,'(BCM) HIGH (#',x,')'
        GPIO.output(relay_02, GPIO.HIGH)
        time.sleep(period)

    GPIO.cleanup()
    print('Exiting...')

except KeyboardInterrupt:
    GPIO.cleanup()
    print('Exiting...')

