import RPi.GPIO as GPIO
import time

relay_01 = 4 # BCM4, pin7
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

GPIO.output(relay_01, GPIO.LOW) # output 0

try:
    while True:
        for x in range(num):
            print 'Set pin',relay_01,'(BCM) HIGH (#',x,')'
            GPIO.output(relay_01, GPIO.HIGH)
            time.sleep(period)
            print 'Set pin',relay_01,'(BCM) LOW (#',x,')'
            GPIO.output(relay_01, GPIO.LOW)
            time.sleep(period)

except KeyboardInterrupt:
   GPIO.cleanup()
   print('Exiting...')

