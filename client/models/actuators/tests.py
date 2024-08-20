import unittest

from irrigation import Irrigation
from air import Air
from arm import Arm, Direction
from lighting import LedMain
from config import *
import time


class IrrigationTest:
    def setUp(self):
        self.irrigation_unit = Irrigation(main_pump_gpio=IrrigationGPIOs.MAIN_PUMP,
                                          water_sol_gpio=IrrigationGPIOs.WATER_SOL,
                                          tank_switch_sol_gpio=IrrigationGPIOs.TANK_SWITCH,
                                          nutr_sol_gpio=IrrigationGPIOs.NUTR_SOL,
                                          levels_sol_gpios=[gpio.value for gpio in LevelSolenoidsGPIOs],
                                          main_tank_empty_gpio=TankSensorGPIOs.MAIN_TANK_SENSOR_EMPTY,
                                          main_tank_full_gpio=TankSensorGPIOs.MAIN_TANK_SENSOR_FULL,
                                          drain_tank_empty_gpio=TankSensorGPIOs.DRAIN_TANK_SENSOR_EMPTY,
                                          drain_tank_full_gpio=TankSensorGPIOs.DRAIN_TANK_SENSOR_FULL)

    def test_irrigation_waterCycle(self):
        self.irrigation_unit.run_cycle(duration=10, levels=[0, 1])


    def test_sol(self, levels):
        for level in levels:
            self.irrigation_unit.levels_sols[level].on()
            time.sleep(5)
            self.irrigation_unit.levels_sols[level].off()

  


class LightingTest:
    def setUp(self):
        self.lighting_unit = LedMain(LightingGPIOs.MAIN_POWER, LightingGPIOs.MAIN_DIM,
                                     LightingGPIOs.SUPP_ONE_DIM, LightingGPIOs.SUPP_TWO_DIM)

    def test_dimming(self):
        self.lighting_unit.power_on()
        time.sleep(5)
        print('dim')


        self.lighting_unit.power_on()

        time.sleep(5)

        self.lighting_unit.power_off()

class FanTest(unittest.TestCase):
    def setUp(self):
        self.air_unit = Air(AIR_MAIN_GPIO)

    def test_fan_on_off(self):
        self.air_unit.on()
        time.sleep(2)
        self.air_unit.off()
        time.sleep(0.5)


irrigation_test = IrrigationTest()
irrigation_test.setUp()
print(irrigation_test.irrigation_unit.levels_sols[2].is_active)
irrigation_test.irrigation_unit.levels_sols[2].on()
print(irrigation_test.irrigation_unit.levels_sols[2].is_active)
time.sleep(2)
irrigation_test.irrigation_unit.levels_sols[2].off()
print(irrigation_test.irrigation_unit.levels_sols[2].is_active)
