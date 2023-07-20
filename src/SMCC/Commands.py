import copy
from bitarray import bitarray
from bitarray.util import int2ba, zeros
from .Constants import ARDUINO_CONSTANTS, DEFAULTS, SOFTWARE_LIMITS

# Commands template

SETUP_BLANK = { #Works as a template for SETUP CMD
    'cmd': [
            bitarray('10000000'), 
            bitarray('00000000'), 
            bitarray('00000000')
            ],
    'response_size': 3, # 3 bytes
}

STEP_BLANK = { #Works as a template for STEP CMD
    'cmd': [
            bitarray('00000000'), 
            bitarray('00000000'), 
            bitarray('00000000')
            ],
    'response_size': 3, # 3 bytes
}

INFO_CMD = {
    'cmd': [
            bitarray('01000000'), # Command packet
            bitarray('00000000'), # Filler packets
            bitarray('00000000')
            ],
    'response_size': 6, # 3 bytes for : setup + freq_counter
                        # 3 bytes for : step + step_counter
}

HALT_CMD = {
    'cmd': [
            bitarray('11000000'), # Command packet
            bitarray('00000000'), # Filler packets
            bitarray('00000000')
            ],
    'response_size': 3, 
}


# Allows to place a boolean flag in a 8bit array
def fillBool(values, start=0):
    padded = bitarray('0000 0000')
    n_bits = len(values)

    if(n_bits + start > 8): 
        raise Exception('Padded value needs more than 8 bits from starting poing {}'.format(start))
    
    for i, bool_val in enumerate(values):
        padded[start+i] = bool_val

    return padded




# Prepares a setup command from control dictionary 
def SETUP_CMD(control_dict):

    # Load template
    setup_cmd = copy.deepcopy(SETUP_BLANK)
    k_cmd, k_r_size = setup_cmd

    # Build the CMD: first byte
    cmd = setup_cmd[k_cmd]
    ms = control_dict['micro_stepping'].value[1]
    flags = fillBool([control_dict['reset'], control_dict['enable'], control_dict['sleep']], 5)    
    cmd[0] |= ms
    cmd[0] |= flags

    # Build the CMD: second byte
    freq_counter_bit = convert2Binary(control_dict['freq_counter'],16)
    cmd[1] |= freq_counter_bit[0:8]
    cmd[2] |= freq_counter_bit[8:16]

    setup_cmd['cmd'] = cmd
    return setup_cmd

# Prepares a step commmand from control dictionary
def STEP_CMD(control_dict):

    # Load template
    step_cmd = copy.deepcopy(STEP_BLANK)
    k_cmd, k_r_size = step_cmd

    # Build the CMD: first byte
    cmd = step_cmd[k_cmd]
    flags = fillBool([control_dict['direction']], 7)
    cmd[0] |= flags

    # Build the CMD: second byte
    steps = convert2Binary(control_dict['steps'],16)
    cmd[1] |= steps[0:8]
    cmd[2] |= steps[8:16]

    step_cmd['cmd'] = cmd

    return step_cmd


# Sends a command through coms
def sendCommand(coms, cmd):
    k_cmd, k_r_size = cmd
    # Write command
    for byte_arr in cmd[k_cmd]:
        coms.write(byte_arr)

    # Wait for automatic reply
    response = coms.read(cmd[k_r_size])
    # Convert the response to bitarrays    
    n_response = []

    for i in response:
        n_response.append(convert2Binary(i, 8))

    # Check if response matches cmd sent
    if(cmd['cmd'] != n_response):
        raise Exception('Response received from controller does not matches sent command.')

    return n_response


# Convert an integer number to binary according to <size>
def convert2Binary(number, size):
    number_bin = int2ba(number)
    if(len(number_bin) < size):
        number_bin = zeros(size - len(number_bin)) + number_bin

    return number_bin


# Gets the requiered frequency by the controller board
def getFrequency(control_dict):
    
    # Calculate requiered frequency by the controller board
    speed = control_dict['speed']
    degrees_per_step = control_dict['degrees_per_step']
    micro_step_factor = control_dict['micro_stepping'].value[2]

    req_freq = (speed*360*micro_step_factor) / (60*degrees_per_step)

    # Calculate freq counter for arduino
    counter = round(ARDUINO_CONSTANTS.CLOCK.value/(req_freq*2*ARDUINO_CONSTANTS.PRESCALER.value) -1)
    real_freq = ARDUINO_CONSTANTS.CLOCK.value/(2*ARDUINO_CONSTANTS.PRESCALER.value*(1+counter))

    return req_freq, real_freq, counter


def generateControlDict():
    driver_controls = {
        'comms': None,
        'micro_stepping': DEFAULTS.MICRO_STEPPING_DEFAULT,
        'reset': DEFAULTS.RESET_DEFAULT.value,  #Logic low for reset
        'enable': DEFAULTS.ENABLE_DEFAULT.value, #Logic low for enable
        'sleep': DEFAULTS.SLEEP_DEFAULT.value, # Logic low for sleep
        'direction': False, #counterclock by default
        'halt': False, # Halt flag
        'speed': SOFTWARE_LIMITS.MIN_SPEED_RPM.value, # 
        'steps': SOFTWARE_LIMITS.MIN_STEPS.value, # Requested number of steps
        'freq': 0, # Frequency for steps
        'freq_counter':0,
        'degrees_per_step': None,
    }

    return driver_controls


def checkConnection(ctrl_dict):
    # Check if comms exists
    if(ctrl_dict['comms'] == None):
        raise Exception('There is no available port to test!')
    
    blank_ctrls = generateControlDict()
    setup_cmd = SETUP_CMD(blank_ctrls)
    # Send command performs comparisson
    sendCommand(ctrl_dict['comms'], setup_cmd)

    # Valid response
    return True