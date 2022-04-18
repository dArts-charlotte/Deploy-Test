import time
import logging
from datetime import datetime, timedelta
from typing import Dict

from sensors.sensors_controller import SensorReader
from sensors.config import SLEEPING_TIME_IN_SECONDS, SAMPLES_FILE_NAME
from actuators.actuator_repository import ActuatorRepository
from actuators.config import *
from csv import DictWriter


class Scheduler:
    irrigation_schedule = IRRIGATION_SCHEDULE
    lighting_schedule = LIGHTING_SCHEDULE
    air_schedule = AIR_SCHEDULE

    sensor_reader = SensorReader()

    # actuator_repo = ActuatorRepository()

    @staticmethod
    def in_time_window(current_time, scheduled_time: datetime.time, sleeping_time=SLEEPING_TIME_IN_SECONDS):
        return True if scheduled_time <= current_time <= scheduled_time + timedelta(seconds=sleeping_time) else False

    def run_actuators(self):
        current_time = datetime.now().time()

        for irrigation_time in self.irrigation_schedule:
            if self.in_time_window(current_time, irrigation_time):
                self.actuator_repo.irrigation.run_water_cycle(duration=WATER_CYCLE_DURATION)
                break

        for air_time in self.air_schedule:
            if self.in_time_window(current_time, air_time):
                [fan.on() for fan in self.actuator_repo.fans]
                break

        for lighting_time_on in [on for (on, off) in self.lighting_schedule]:
            if self.in_time_window(current_time, lighting_time_on):
                self.actuator_repo.main_led.on()
                break
        for lighting_time_off in [off for (on, off) in self.lighting_schedule]:
            if self.in_time_window(current_time, lighting_time_off):
                self.actuator_repo.main_led.off()
                break

    def store_samples(self, samples: Dict, file_name: str):
        with open(file_name, 'a') as csv_file:
            fields = samples.keys()
            dict_writer = DictWriter(csv_file, fields)
            dict_writer.writerow(samples)
            csv_file.close()

    def run(self):
        while True:
            samples = Scheduler.sensor_reader.run()
            print(samples)  # TODO replace with pymongo
            self.store_samples(samples, SAMPLES_FILE_NAME)
            time.sleep(SLEEPING_TIME_IN_SECONDS)


if __name__ == "__main__":
    Scheduler().run()
