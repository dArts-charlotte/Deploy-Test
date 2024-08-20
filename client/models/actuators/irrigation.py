from typing import List

# from .lighting import LedMain
import gpiozero
from gpiozero import DigitalOutputDevice
from gpiozero import DigitalInputDevice
import time
import logging
import os
import sys
# Modify PATH so we can import files from elsewhere in this repo
from os.path import dirname, join, abspath
from models.actuators.config import IRRIGATION_LEVEL_OFFSET

sys.path.insert(0, abspath(join(dirname(__file__), '../..')))


class Irrigation:

    def __init__(self, water_sol_gpio, tank_switch_sol_gpio, nutr_sol_gpio,
                 levels_sol_gpios: List,
                 pressure_relief_gpio
                 ):
        self.water_sol = DigitalOutputDevice(water_sol_gpio)
        self.pressure_relief_sol = DigitalOutputDevice(pressure_relief_gpio)
        self.tank_switch_sol = DigitalOutputDevice(tank_switch_sol_gpio)
        self.nutr_sol = DigitalOutputDevice(nutr_sol_gpio)
        self.levels_sols = [DigitalOutputDevice(level_sol_gpio) for level_sol_gpio in levels_sol_gpios]



    def run_cycle(self, duration, nutrient=False, levels=None):
        source_sol = self.nutr_sol if nutrient else self.water_sol
        levels_sols = [self.levels_sols[level-1] for level in levels] if levels else self.levels_sols
        primeTime = 15
        source_sol.on()
        time.sleep(20)
        levels = range(1, 9) if not levels else levels
        levels = list(reversed(levels))
        for i,level in enumerate(levels):
            sol = self.levels_sols[level - 1]
            level_duration = duration + IRRIGATION_LEVEL_OFFSET[level]
            print(f'Prime Process running for level {level}')
            self.pressure_relief_sol.on()
            print('Pressure relief sol is on!')
            sol.on()
            print(f'Solenoid level {level} is on!')
            print(f'Sleeping for {primeTime}...')

            time.sleep(primeTime)
            self.pressure_relief_sol.off()
            print('Pressure relief sol is off!')

            print(f'Sleeping for {level_duration}...')

            time.sleep(level_duration)
            sol.off()
            print(f'Solenoid level {level} is off!')

            print(f'draingin level {level}!')

            time.sleep(1)
            self.pressure_relief_sol.on()
            print('Pressure relief sol is on!')

            time.sleep(20)
            self.pressure_relief_sol.off()
            print('Pressure relief sol is off!')

            time.sleep(1)

        source_sol.off()


    def run_cycle_level(self, level_sol, duration):
        pass


    def sol_check(self):
        for sol in self.levels_sols:
            sol.off()
            print(sol, 'off')
            time.sleep(1)
        self.water_sol.off()
        print('water_sol_off')
