# Required imports
import serial
import serial.tools.list_ports
import pprint
import time
from SMCC.Commands import SETUP_CMD, STEP_CMD, generateControlDict, checkConnection, getFrequency, sendCommand


# 1 -> Generate control dict 
ctrl_dict = generateControlDict()

print('[INFO] Generated dictionary:')
pprint.pprint(ctrl_dict)

# 2 -> Configure for particular motor characteristics 
while True:
    deg_per_step = input('[USER] Type the number of degrees per step taken by the motor: ')
    try:
        ctrl_dict['degrees_per_step'] = float(deg_per_step)
        break
    except:
        print('[ERROR] Not a valid value!')

# 3 -> Connect to arduino serial port 

# Get all available ports -- This part is only used as an example if you don't
# know which port your Arduino is connected to!

available_ports = serial.tools.list_ports.comports()

# List all the ports for the user to select
print('[INFO] Select the serial port to which the Arduino is connected to:')
ports = []
for i, value in enumerate(available_ports):
    port, _, _ = value
    ports.append(port)
    print('{}.- {}'.format(i, port))

# Allow user to select port
port_selection = int(input('[INFO] Select the port from the list above: '))

# Lock user until valid port is selected
while(True):
    if(port_selection < len(ports)):
        port_name = ports[port_selection]
        print('[INFO] The selected port is {}'.format(port_name))
        break
    else:
        print('[ERROR] Not a valid selection, try again!')

# Connect to the selected serial port
baud_rate = 9600
timeout = 10.0 # seconds

ctrl_dict['comms'] = serial.Serial(port, baudrate=baud_rate, timeout=timeout)
# Wait 10 seconds for the Arduino to reboot
print('[INFO] Waiting (10s) for the Arduino to reboot ...')
time.sleep(10)
print('[INFO] Performing connection test ...')

# Check if the controller can respond:
if(checkConnection(ctrl_dict)): 
    print('[INFO] Connection sucessful! Controller is talking to the host.')

# 4 -> Configure the motor for 10 rpm operation

speed = 10 #rpm
ctrl_dict['speed'] = speed
# With the speed the operation frequency for the controller can be set:

req_freq, real_freq, counter = getFrequency(ctrl_dict)

print('[INFO] Required frequency for {} rpm operation is {} Hz'.format(speed, req_freq))
print('[INFO] Factible frequency for controller is {} Hz'.format(real_freq))
print('[INFO] Frequency counter is set to {}'.format(counter))

# Add the frequency and counter to the control dict
ctrl_dict['freq'] = real_freq
ctrl_dict['freq_counter'] = counter

# Configure the controller with this information
setup_cmd = SETUP_CMD(ctrl_dict)
print('[INFO] Setup cmd is:')
pprint.pprint(setup_cmd)

setup_response = sendCommand(ctrl_dict['comms'], setup_cmd)
print('[INFO] Controller response is :')
pprint.pprint(setup_response)

# The controller always repply with the configuration performed, the sendCommand function check if they are equal
# if not an exception is raised!
print('[INFO] Response matches command sent!')
# 5 -> Step 1 full rotation clockwise
steps = 96
ctrl_dict['steps'] = steps
ctrl_dict['direction'] = True

# Generate step cmd
step_cmd = STEP_CMD(ctrl_dict)
print('[INFO] Step cmd is :')
pprint.pprint(step_cmd)

step_response = sendCommand(ctrl_dict['comms'], step_cmd)
print('[INFO] Controller response is :')
pprint.pprint(step_response)


wait_before_close = 20 #seconds
print('[INFO] Program will wait {} seconds before closing the serial port to allow the motor to perform the steps'.format(wait_before_close))
time.sleep(wait_before_close)

# Close the port
ctrl_dict['comms'].close()

