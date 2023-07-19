# SMCC

<p align=center>
    <img src='https://raw.githubusercontent.com/Wauro21/SMCC/master/github_images/icon.png'>
</p>

The **SMCC (SMC-Core)** is a simple python based API that allows to interface via serial port with the [**SMCD (SMC-Driver)**](https://github.com/Wauro21/SMCD). This allows the **SMCC** to be imported to your own projects without having to drag the GUI with it.


## Index

- [SMCC](#smcc)
  - [Index](#index)
  - [Installation](#installation)
  - [Example use](#example-use)
    - [Quick Start](#quick-start)
    - [In depth examples](#in-depth-examples)
  - [Reference](#reference)


## Installation

To install the `SMCC` just use pip as follows: 

```bash
$ pip install smcc

```

The project is hosted on the pypi register: https://pypi.org/projects/smcc


## Example use

### Quick Start

Configure a 3.75°/step stepper motor to perform a full clockwise rotation at 20 rpm:

```python
# Imports
import serial
import time
from SMCC.Commands import SETUP_CMD, STEP_CMD, generateControlDict, sendCommand

# Configure motor
ctrl_dict = generateControlDict()
ctrl_dict['degrees_per_step'] = 3.75

# Serial port configuration
port='/dev/ttyACM0'
br = 9600
to = 10 # seconds
ctrl_dict['comms'] = serial.Serial(port, baudrate=br, timeout=to)
# Wait 10 seconds for Arduino to reboot
time.sleep(10)

# Configure speed
ctrl_dict['speed'] = 20
# Configure freq from speed
_, real_freq, counter = getFrequency(ctrl_dict)
ctrl_dict['freq'] = real_freq
ctrl_dict['freq_counter'] = counter

# Send setup CMD
setup_cmd = SETUP_CMD(ctrl_dict)
setup_response = sendCommand(ctrl_dict['comms'], setup_cmd)

# Set rotation direction and number of steps
n_steps = int(360/ctrl_dict['degrees_per_step'])
ctrl_dict['steps'] = n_steps
ctrl_dict['direction'] = True

# Send step cmd
step_cmd = STEP_CMD(ctrl_dict)
step_response = sendCommand(ctrl_dict['comms'], step_cmd)

# Wait for the motor to complete rotation before closing port
wait_time = 20 #Seconds
time.sleep(wait_time)

ctrl_dict['comms'].close()

```

### In depth examples


Two detailed explained examples are provided on [Examples](https://github.com/Wauro21/SMCC/tree/master/Examples):

1. `python_example.py` : Shows the basic operation of the API, by performing the configuration and then a full counterclockwise rotation of the stepper motor. 
2. `jupyter_example.ipynb`: Shows the basic operation of the API, performs a clockwise and then a counterclockwise rotation of the stepper motor. 

**All the examples are designed to work with the [`SMCD (Serial Motor Controller Driver)`](https://github.com/Wauro21/SMCD)**

## Reference

The [REFERENCE.md](https://github.com/Wauro21/SMCC/tree/master/REFERENCE.md) provides a detailed explanation of every function and constant provided on the API.  

