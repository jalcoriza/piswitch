#
# Base file to control the raspberrypi's GPIO
# python3 code
#
import RPi.GPIO as GPIO
import time
import datetime
import csv

relay_01 = 4 # BCM4, pin7, OUT-01, bulb light
relay_02 = 17 # BCM17, pin11, OUT-02, garage door #1
relay_03 = 27 # BCM27, pin13, OUT-03, door #2
relay_04 = 22 # BCM22, pin15, OUT-04
relay_05 = 10 # BCM10, pin19, OUT-05
input_01 = 9 # BCM9, pin21, IN-01, short input
input_02 = 11 # BCM11, pin23, IN-02, long input

period = 0.5 # Period in seconds
t = 0

door_hysteresis = False
door_count = 0
door_time = 2
door2_hysteresis = False
door2_count = 0
door2_time = 2

pir_hysteresis = False
pir_count = 0
pir_time = 60
pir_time_begin = datetime.datetime.strptime('20:00', '%H:%M').time()
pir_time_end = datetime.datetime.strptime('08:00', '%H:%M').time()

command_file_str = '/home/pi/Projects/piswitch/command.csv'

output_gpio = [GPIO.HIGH, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH]
input_gpio = [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW] # input_01(IN-01), input_02(IN-02), light_on(csv), light_off(csv), door(csv), door2 (csv)

def show_variables():
    global period
    global t
    global door_hyteresis
    global door_count
    global door_time
    global pir_hyteresis
    global pir_count
    global pir_time
    global pir_time_begin
    global pir_time_end

    print(f'period={period}s, t={t}')
    print(f'door_hysteresis={door_hysteresis}, door_count={door_count}, door_time={door_time}')
    print(f'pir_hysteresis={pir_hysteresis}, pir_count={pir_count}, pir_time={pir_time}')
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

def read_command():

    return 0


def read_command2():
    global command_file_str;

    with open(command_file_str, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        # Beta implementation. Only process one command per file!
        # Row fromat
        # written|read, who    , n --> input[n], value
        # w|r         , jav|dan, [2-4]         , 0|1
        for row in csv_reader:
            print(f'{datetime.datetime.now()} raw_command=,{row}')
            if row[0] == 'r': # new command
                print(f'{datetime.datetime.now()} new command!')
                row[0] = 'w' # mark the command as done

            if int(row[2]) == 2: # light on command
                print(f'{datetime.datetime.now()} command=light,{row[3]}')
                input_gpio[2] = int(row[3]) 

            elif int(row[2]) == 3: # light off command
                print(f'{datetime.datetime.now()} command=light,{row[3]}')
                input_gpio[3] = int(row[3]) 

            elif int(row[2]) == 4: # door command
                print(f'{datetime.datetime.now()} command=door,{row[3]}')
                input_gpio[4] = int(row[3]) 

            elif int(row[2]) == 5: # door2 command
                print(f'{datetime.datetime.now()} command=door,{row[3]}')
                input_gpio[5] = int(row[3]) 

            line_count += 1

        
        print(f'{datetime.datetime.now()} Processed {line_count} lines')

        # Save a copy of the read content
        # check it - it doesn't work
        lines = list(csv_reader)
        print(f'{datetime.datetime.now()} Save lines= {lines}')
                
    with open(command_file_str, mode='w') as csv_file:
        print(f'{datetime.datetime.now()} Updating csv file')

        line_count = 0
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
        for row in lines:
            csv_writer.writerow(row)
            line_count += 1

        print(f'{datetime.datetime.now()} Updated csv file with {line_count} lines')

    return 0


def status_gpio():
    print(f'{datetime.datetime.now()} input={input_gpio} output={output_gpio}')

    return 0

def process_door():
    global door_hysteresis
    global door_count
    global door_time

    if (door_hysteresis): 
        door_count += 1;
        if (door_count * period) > door_time:
            door_hysteresis = False
            door_count = 0
            input_gpio[4] = GPIO.LOW

    else:
        if (input_gpio[4] == GPIO.HIGH):
            output_gpio[1] = GPIO.LOW
            door_hysteresis = True
            print(f'{datetime.datetime.now()} Open/Close the door!')

        else:
            output_gpio[1] = GPIO.HIGH
            print(f'{datetime.datetime.now()} Reseting the door\'s relay!')
                
    return 0

def process_door2():
    global door2_hysteresis
    global door2_count
    global door2_time

    if (door2_hysteresis): 
        door2_count += 1;
        if (door2_count * period) > door2_time:
            door2_hysteresis = False
            door2_count = 0
            input_gpio[5] = GPIO.LOW

    else:
        if (input_gpio[5] == GPIO.HIGH):
            output_gpio[2] = GPIO.LOW
            door2_hysteresis = True
            print(f'{datetime.datetime.now()} Open/Close the door2!')

        else:
            output_gpio[2] = GPIO.HIGH
            print(f'{datetime.datetime.now()} Reseting the door2\'s relay!')
                
    return 0

def process_pir():
    global pir_hysteresis
    global pir_count
    global pir_time
    global pir_time_begin
    global pir_time_end

    time_now = datetime.datetime.now().time()
    if (input_gpio[2] == GPIO.HIGH) and (input_gpio[3] == GPIO.LOW):
        output_gpio[0] = GPIO.LOW
        
    elif (input_gpio[3] == GPIO.HIGH):
        output_gpio[0] = GPIO.HIGH
        input_gpio[2] = GPIO.LOW
        input_gpio[3] = GPIO.LOW

    elif (time_now > pir_time_begin) or (time_now < pir_time_end):  
        if (pir_hysteresis): 
            pir_count += 1;
            if (pir_count * period) > pir_time:
                pir_hysteresis = False
                pir_count = 0

        else:
            if (input_gpio[0] == GPIO.HIGH):
                output_gpio[0] = GPIO.LOW
                pir_hysteresis = True
                print(f'{datetime.datetime.now()} detected movement! turn on the light!')

            else:
                output_gpio[0] = GPIO.HIGH

    else:
        print(f'{datetime.datetime.now()} now={time_now} is outside ({pir_time_begin},{pir_time_end})')


    return 0

def process_automaton():
    process_door()
    process_door2()
    process_pir()

    return 0


# Initialize GPIO outputs to HIGH (it doesn't activate the relays)
# main() code

print('Initializing GPIO...')
show_variables()
init_gpio()

print('Initializing relays OUTPUT as HIGH...')
write_gpio()

try:
    # Infinite loop waiting for a CTRL^C
    while True:
        process_automaton()

        t += 1
        write_gpio()
        read_gpio()
        read_command2()
        status_gpio()
        time.sleep(period)

except KeyboardInterrupt:
   GPIO.cleanup()
   print('Exiting...')

