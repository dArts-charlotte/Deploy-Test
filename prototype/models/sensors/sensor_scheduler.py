from apscheduler.schedulers.background import BackgroundScheduler
from models.sensors.sensors_controller import sensor_reader
from csv import DictWriter
from typing import Dict
from models.sensors.config import *

class SensorScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.create_sensor_reader_job(interval_time=SLEEPING_TIME_IN_SECONDS)
        self.status = False
        self.initiated = False

    def create_sensor_reader_job(self, interval_time):
        def read_and_publish():
            samples = sensor_reader.read_sensors()
            print(samples)

            #TODO send samples to the serv

        self.scheduler.add_job(read_and_publish, 'interval', seconds=interval_time, id='sensor_job')


    def store_samples(self, samples: Dict, file_name: str):
        with open(file_name, 'a') as csv_file:
            fields = samples.keys()
            dict_writer = DictWriter(csv_file, fields)
            dict_writer.writerow(samples)
            csv_file.close()

    def modify_sensor_reader_job(self):
        raise NotImplementedError


    def start(self):
        if not self.status:
            self.scheduler.start() if not self.initiated else self.scheduler.resume()
            self.status = True
            self.initiated = True


    def pause(self):
        if self.status:
            self.scheduler.pause()
            self.status = False

sensor_scheduler = SensorScheduler()
