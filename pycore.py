#
# Base file to control the raspberrypi's GPIO
# python3 code
#
import RPi.GPIO as GPIO
import time
import datetime

relay_01 = 4 # BCM4, pin7, OUT-01, bulb light
relay_02 = 17 # BCM17, pin11, OUT-02, garage door
relay_03 = 27 # BCM27, pin13, OUT-03
relay_04 = 22 # BCM22, pin15, OUT-04
relay_05 = 10 # BCM10, pin19, OUT-05
input_01 = 9 # BCM9, pin21, IN-01, short input
input_02 = 11 # BCM11, pin23, IN-02, long input

period = 0.5 # Period in seconds
t = 0
hysteresis = False
pir_count = 0
pir_time = 60
pir_time_begin = datetime.datetime.strptime('21:00', '%H:%M').time()
pir_time_end = datetime.datetime.strptime('07:00', '%H:%M').time()

def show_variables():
    global hyteresis
    global period
    global t
    global pir_count
    global pir_time
    global pir_time_begin
    global pir_time_end

    print(f'period={period}s, t={t}')
    print(f'hysteresis={hysteresis}, pir_count={pir_count}, pir_time={pir_time}')
    print(f'pir_time_begin={pir_time_begin}, pir_time_end={pir_time_end}')

    return 0

def init_gpio():
    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_01, GPIO.OUT) # GPIO assign mode
    GPIO.setup(relay_02, GPIO.OUT) # GPIO assign mode
    GPIO.setup(relay_03, GPIO.OUT) # GPIO assign mode
    GPIO.setup(relay_04, GPIO.OUT) # GPIO assign mode
    GPIO.setup(relay_05, GPIO.OUT) # GPIO assign mode
    GPIO.setup(input_01, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # input with pull-down 
    GPIO.setup(input_02, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # input with pull-down 

    return 0

def write_gpio():
    GPIO.output(relay_01, output_gpio[0])
    GPIO.output(relay_02, output_gpio[1])
    GPIO.output(relay_03, output_gpio[2])
    GPIO.output(relay_04, output_gpio[3])
    GPIO.output(relay_05, output_gpio[4])

    return 0

def read_gpio():
    input_gpio[0] = GPIO.input(input_01)
    input_gpio[1] = GPIO.input(input_02)

    return 0

def status_gpio():
    print(f'{datetime.datetime.now()} input={input_gpio} output={output_gpio}')

    return 0

def process_pir():
    global hysteresis
    global pir_count
    global pir_time_begin
    global pir_time_end

    time_now = datetime.datetime.now().time()
    if (time_now > pir_time_begin) or (time_now < pir_time_end):  
        if (hysteresis): 
            pir_count += 1;
            if (pir_count * period) > pir_time:
                hysteresis = False
                pir_count = 0

        else:
            if (input_gpio[0]==GPIO.HIGH):
                output_gpio[0] = GPIO.LOW
                hysteresis = True
                print(f'{datetime.datetime.now()} detected movement! turn on the light!')

            else:
                output_gpio[0] = GPIO.HIGH

    else:
        print(f'{datetime.datetime.now()} now={time_now} is outside ({pir_time_begin},{pir_time_end})')


    return 0

def process_automaton():
    process_pir()

    return 0


# Initialize GPIO outputs to HIGH (it doesn't activate the relays)
# main() code

output_gpio = [GPIO.HIGH, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH]
input_gpio = [GPIO.LOW, GPIO.LOW]

print('Initializing GPIO...')
show_variables()
init_gpio()

print('Initializing relays OUTPUT as HIGH...')
write_gpio()

try:
    # Infinite loop waiting for a CTRL^C
    while True:
        #print(f'Set pin {relay_01} (BCM) LOW (t={t * period}s)')
        #output_gpio[0] = GPIO.LOW
        process_automaton()

        t += 1
        write_gpio()
        read_gpio()
        status_gpio()
        time.sleep(period)

except KeyboardInterrupt:
   GPIO.cleanup()
   print('Exiting...')

