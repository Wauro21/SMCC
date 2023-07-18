from enum import Enum
from bitarray import bitarray

# Constants for Arduino board
class ARDUINO_CONSTANTS(Enum):
    CLOCK = 16000000 # Default clock
    PRESCALER = 64 # Prescaler for timer1

# Defines the pinout for each microstepping selection
class MICROSTEPPING(Enum):
    FULL_STEP = ['Full-Step', bitarray('00 000 000'), 1]
    HALF_STEP = ['Half-Step',bitarray('00 001 000'), 2]
    QUARTER_STEP = ['1/4 Step', bitarray('00 010 000'), 4]
    EIGHT_MICRO = ['1/8 Step', bitarray('00 011 000'), 8]
    SIXTEEN_MICRO = ['1/16 Step', bitarray('00 100 000'), 16]
    THIRTY_TWO_MICRO = ['1/32 Step', bitarray('00 111 000'), 32] # Can be 101 - 110 -


class SOFTWARE_LIMITS(Enum):
    MAX_SPEED_RPM = 50
    MIN_SPEED_RPM = 1
    MAX_STEPS = 32767 # This is by the register size
    MIN_STEPS = 0


class DEFAULTS(Enum):
    # Defaults for controller
    MICRO_STEPPING_DEFAULT = MICROSTEPPING.FULL_STEP.value # Full step
    RESET_DEFAULT = True # not-reseted
    ENABLE_DEFAULT = False # Enabled
    SLEEP_DEFAULT = True # Disable sleep
