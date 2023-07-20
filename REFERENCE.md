# API Reference

<p align=center>
    <img src='https://raw.githubusercontent.com/Wauro21/SMCC/master/github_images/icon.png'>
</p>

- [API Reference](#api-reference)
  - [Functions](#functions)
    - [1. `filBool(value, start=0)`](#1-filboolvalue-start0)
    - [2. `SETUP_CMD(control_dict)`](#2-setup_cmdcontrol_dict)
    - [3. `STEP_CMD(control_dict)`](#3-step_cmdcontrol_dict)
    - [4. `sendCommand(coms, cmd)`](#4-sendcommandcoms-cmd)
    - [5. `convert2Binary(number, size)`](#5-convert2binarynumber-size)
    - [6. `getFrequency(control_dict)`](#6-getfrequencycontrol_dict)
    - [7. `generateControlDict()`](#7-generatecontroldict)
    - [8. `checkConnection(ctrl_dict)`](#8-checkconnectionctrl_dict)
  - [Templates](#templates)
    - [1. `SETUP_BLANK`:](#1-setup_blank)
    - [2. `STEP_BLANK`:](#2-step_blank)
    - [3. `INFO_CMD`:](#3-info_cmd)
    - [4. `HALT_CMD`:](#4-halt_cmd)
  - [Constants](#constants)
    - [1. `ARDUINO_CONSTANTS`](#1-arduino_constants)
    - [2. `MICROSTEPPING`](#2-microstepping)
    - [3. `SOFTWARE_LIMITS`](#3-software_limits)
    - [4. `DEFAULTS`](#4-defaults)



## Functions

### 1. `filBool(value, start=0)`

Position a list of booleans inside a byte starting from `start`. 

```
# Pseudo-code example

flags = [True, False, True, True]
start = 2

# byte position is 0123_4567
# byte value is    0000_0000

print(fillBool(flags, start))

# This returns 0010_1100


```

**Parameters:**
- `value`: A list of booleans
- `start=0`: Starting poisition inside the byte. Default is zero

**Returns:** A bitarray element

### 2. `SETUP_CMD(control_dict)`

Returns a SETUP Command with the `control_dict` configurations. Mainly the reset, enable, sleep, frequency and frequency counter information.

**Parameters:**
- `control_dict`: Dictionary that groups all the controlable elements of the SMC-Driver.

**Returns:** A dictionary with the setup command with the information of ctrl_dict and the number of bytes expected for the controller response. The dictionary is based on the `SETUP_BLANK` with the `control_dict` information written on top.

### 3. `STEP_CMD(control_dict)`

Returns a STEP Command with the `control_dict` configurations. Mainly the direction and step counter information.

**Parameters:**
- `control_dict`: Dictionary that groups all the controlable elements of the SMC-Driver.

**Returns:** A dictionary with the step command with the information of ctrl_dict and the number of bytes expected for the controller response. The dictionary is based on the `STEP_BLANK` with the `control_dict` information written on top.

### 4. `sendCommand(coms, cmd)`

Sends the desired command `cmd` via the `coms` serial port.

**Parameters:**
- `coms`: A PySerial serial port connection. Typically corresponds to `ctrl_dict['comms']`.
- `cmd`: The desired command to send. Values can be: `SETUP_CMD`, `STEP_CMD`, `INFO_CMD` and `HALT_CMD`.

**Returns:** The bytes associated with the controller response. 

### 5. `convert2Binary(number, size)`

Converts the integer stored on `number` to a binary number of `size` bits. 

**Parameters:**
- `number`: Integer number to convert
- `size`: Size in bits of the resulting binary number.

**Returns:** The converted binary number with `size` bits.

### 6. `getFrequency(control_dict)`

Calculates the requiered frequency for a specific `control_dict['speed']` and `control_dict['degrees_per_step']`. Uses the following formula found on the [DRV8825 Datasheet](https://www.ti.com/lit/ds/symlink/drv8825.pdf) to calculate the square wave use to step the motor:

$$
f_{step} = \frac{v (rotation/minute) \times 360 (°/rotation) \times n_{m} (\mu steps/step)}{60 (seconds/minute) \times \theta (°/step)}
$$

**Parameters:**
- `control_dict`: Dictionary that groups all the controlable elements of the SMC-Driver. Mainly the speed and degrees per step characteristics of the motor are used.

**Returns:**
- `req_freq`: The theorical requiered frequency obtained through the datasheet formula.
- `real_freq`: The factible frequency achievable with the Arduino timer.
- `freq_counter`: The frequency counter requiered by the `real_freq` to generate the square wave on the controller. 

### 7. `generateControlDict()`

Generates a default  control dictionary.

**Returns:** 
```python
{
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
```

### 8. `checkConnection(ctrl_dict)`

Performs a serial connection check by sending a default SETUP_CMD to the controller and waiting for the response.

**Parameters:**
- `ctrl_dict`: The control dictionary. The `'comms'` must be set (serial port must be open). 

**Returns**: True if the connection was sucessful. If not, raises an Exception.

## Templates

### 1. `SETUP_BLANK`: 

Works as a template for the SETUP command. **To generate a SETUP command is recommended to use the SETUP_CMD function instead.**

```python
SETUP_BLANK = {
    'cmd': [
            bitarray('10000000'), 
            bitarray('00000000'), 
            bitarray('00000000')
            ],
    'response_size': 3, # 3 bytes
}
```

The list holds a blank setup command, that can be customized to the desired setup-command. It also holds the response size in bytes. 

**Example use:**

```python
import copy
from SMCC.Commands import SETUP_BLANK

# from the blank always use deepcopy to create a separate instance of the SETUP_BLANK. 

derived_setup_cmd = copy.deepcopy(SETUP_BLANK)

```

### 2. `STEP_BLANK`: 

Works as a template for the STEP command. **To generate a STEP command is recommended to use the STEP_CMD function instead.**

```python
STEP_BLANK = { 
    'cmd': [
            bitarray('00000000'), 
            bitarray('00000000'), 
            bitarray('00000000')
            ],
    'response_size': 3, # 3 bytes
}
```

The list holds a blank step command, that can be customized to the desired setup-command. It also holds the response size in bytes. 

**Example use:**

```python
import copy
from SMCC.Commands import STEP_BLANK

# from the blank always use deepcopy to create a separate instance of the STEP_BLANK. 

derived_setup_cmd = copy.deepcopy(STEP_BLANK)
```

### 3. `INFO_CMD`: 

Indicates the structure of the INFO Command. The controller responds this command with the SETUP information (control information, frequency, frequency counter) and the current STEP information (number of steps and direction)

```python
INFO_CMD = {
    'cmd': [
            bitarray('01000000'), # Command packet
            bitarray('00000000'), # Filler packets
            bitarray('00000000')
            ],
    'response_size': 6, # 3 bytes for : setup + freq_counter
                        # 3 bytes for : step + step_counter
}
```

The response size corresponds to 6 bytes: 
- 3 bytes for setup information and frequency counter
- 3 bytes for step information and number of steps to take

**Example use:**

```python
import copy
from SMCC.Commands import INFO_CMD, sendCommand

# We assume an established serial port on ctrl_dict

info_response = sendCommand(ctrl_dict['comms'], INFO_CMD)
```

### 4. `HALT_CMD`: 

Indicates the structure of the HALT Command. When sent the controller stops all motor operations.

```python
HALT_CMD = {
    'cmd': [
            bitarray('11000000'), # Command packet
            bitarray('00000000'), # Filler packets
            bitarray('00000000')
            ],
    'response_size': 1,
}
```

**Example use:**

```python
import copy
from SMCC.Commands import HALT_CMD, sendCommand

# We assume an established serial port on ctrl_dict

info_response = sendCommand(ctrl_dict['comms'], HALT_CMD)
```



## Constants

The constants are implemented as `Enum Classes`.

### 1. `ARDUINO_CONSTANTS`

Holds the Arduino clock value and prescaler for Timer1.

```python
class ARDUINO_CONSTANTS(Enum):
    CLOCK = 16000000 # Default clock
    PRESCALER = 64 # Prescaler for timer1
```

### 2. `MICROSTEPPING`

Indicates all the possible micro-stepping options for the controller. 

```python
class MICROSTEPPING(Enum):
    FULL_STEP = ['Full-Step', bitarray('00 000 000'), 1]
    HALF_STEP = ['Half-Step',bitarray('00 001 000'), 2]
    QUARTER_STEP = ['1/4 Step', bitarray('00 010 000'), 4]
    EIGHT_MICRO = ['1/8 Step', bitarray('00 011 000'), 8]
    SIXTEEN_MICRO = ['1/16 Step', bitarray('00 100 000'), 16]
    THIRTY_TWO_MICRO = ['1/32 Step', bitarray('00 111 000'), 32] # Can be 101 - 110 -
```

### 3. `SOFTWARE_LIMITS`

The software limits are use to set the max and min rpm values for speed and the maximum number of steps (set by the available bits on the step counter in the controller).

```python
class SOFTWARE_LIMITS(Enum):
    MAX_SPEED_RPM = 50
    MIN_SPEED_RPM = 1
    MAX_STEPS = 65535 # This is by the register size (unsigned 16 bit)
    MIN_STEPS = 0
```

### 4. `DEFAULTS`

Default values use mainly on the `ctrl_dict` generation:

```python
class DEFAULTS(Enum):
    # Defaults for controller
    MICRO_STEPPING_DEFAULT = MICROSTEPPING.FULL_STEP.value # Full step
    RESET_DEFAULT = True # not-reseted
    ENABLE_DEFAULT = False # Enabled
    SLEEP_DEFAULT = True # Disable sleep
```

