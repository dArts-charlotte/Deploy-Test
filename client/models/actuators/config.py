from enum import Enum



class LightingGPIOs:
    MAIN_POWER = 19
    # MAIN_DIM = 25
    # SUPP_ONE_DIM = 13
    # SUPP_TWO_DIM = 12


class IrrigationGPIOs:
    WATER_SOL = 17
    PRESS_RELIEF = 5
    NUTR_SOL = 27
    TANK_SWITCH = 14                                                             
    # TODO


class TankSensorGPIOs:
    MAIN_TANK_SENSOR_FULL = 20
    MAIN_TANK_SENSOR_EMPTY = 5
    # Drain Supply Sensors
    #DRAIN_TANK_SENSOR_FULL = 16
    #DRAIN_TANK_SENSOR_EMPTY = 26


class LevelSolenoidsGPIOs(Enum):
    LEVEL_1 = 22
    LEVEL_2 = 23
    LEVEL_3 = 24
    LEVEL_4 = 25
    LEVEL_5 = 16
    LEVEL_6 = 8
    LEVEL_7 = 9
    LEVEL_8 = 18


class ArmGPIOs:
    ENABLE = 10
    DIRECTION = 24
    PULSE = 21
    LEFT_LIMIT = 8
    RIGHT_LIMIT = 11


AIR_MAIN_GPIO = 26

DEFAULT_WATER_CYCLE_DURATION = 30
IRRIGATION_SCHEDULE = [
#     ("00:30:00", DEFAULT_WATER_CYCLE_DURATION),
    ("06:30:00", DEFAULT_WATER_CYCLE_DURATION),
   # ("10:30:00", 60),

   # ("14:30:00", DEFAULT_WATER_CYCLE_DURATION),
   # ("19:00:00", DEFAULT_WATER_CYCLE_DURATION),
    ("22:30:00", DEFAULT_WATER_CYCLE_DURATION),
    ]

IRRIGATION_LEVEL_OFFSET = {
    1: 0,#30,
    2: 0,#,35,
    3: 0,#40,
    4: 0,#45,
    5: 30,
    6: 35,
    7: 40,
    8: 65

}
LIGHTING_SCHEDULE = [
    ("08:00:00", "18:30:00")
]
AIR_SCHEDULE = [
    #("07:00:00", "10:00:00")
]
