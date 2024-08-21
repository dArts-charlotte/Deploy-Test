import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime
from typing import Dict, List
from csv import DictWriter
from .actuator_controller import actuator_controller
from .config import *

from .dataaccess import sqlite

logging.basicConfig(filename='amps_v2.log',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)





class ActuatorScheduler:

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.immediate_scheduler = BackgroundScheduler()
        self.irrigation_schedule = []
        self.lighting_schedule = []
        self.air_schedule = []

        with sqlite.get_database_connection() as conn:
            self.load_air_schedule(conn)
            self.load_irrigation_schedule(conn)
            self.load_lighting_schedule(conn)
        

        self.add_irrigation_jobs(irrigation_schedule=self.irrigation_schedule, alter=False)
        self.add_air_jobs(air_schedule=self.air_schedule, alter=False)
        self.add_lighting_jobs(lighting_schedule=self.lighting_schedule, alter=False)
        self.status = False
        self.initiated = False

    def load_irrigation_schedule(self, conn):
        IRRIGATION_SCHEDULE = sqlite.load_irrigation_schedule(conn)
        self.irrigation_schedule = [(datetime.strptime(cycle_time, "%H:%M:%S"), duration) for cycle_time, duration in
                               IRRIGATION_SCHEDULE]

    def load_lighting_schedule(self, conn):
        LIGHTING_SCHEDULE = sqlite.load_lighting_schedule(conn)
        print(LIGHTING_SCHEDULE)
        self.lighting_schedule = [(datetime.strptime(time_on, "%H:%M:%S"), datetime.strptime(time_off, "%H:%M:%S"))
                             for time_on, time_off in LIGHTING_SCHEDULE]
        print('self', self.lighting_schedule)

    def load_air_schedule(self, conn):
        AIR_SCHEDULE = sqlite.load_air_schedule(conn)  # If you have entries for air schedule
        self.air_schedule = [(datetime.strptime(time_on, "%H:%M:%S"), datetime.strptime(time_off, "%H:%M:%S"))
                             for time_on, time_off in AIR_SCHEDULE]

    def reinitiate_state(self):
        current_time = datetime.now().time()
        print("schedule starts")

        for scheduled_window in self.air_schedule:
            if scheduled_window[0].time() <= current_time <= scheduled_window[1].time():
                actuator_controller.air_controller.on()
                print('fans on')
                break
        else:
            actuator_controller.air_controller.off()
            print('fans off')

        for scheduled_window in self.lighting_schedule:
            if scheduled_window[0].time() <= current_time <= scheduled_window[1].time():
                actuator_controller.led_controller.power_on()
                print('lights on')
                break
        else:
            actuator_controller.led_controller.power_off()
            print('lights off')

    @staticmethod
    def turn_off_actuators():
        actuator_controller.air_controller.off()
        actuator_controller.led_controller.power_off()

    @staticmethod
    def valid_schedule(time_schedule: List):
        """
        checks if there are overlaps in the schedule and if the window is valid or not
        """
        time_schedule.sort()
        for i in range(len(time_schedule) - 1):
            if time_schedule[i][0] >= time_schedule[i][1]:
                raise Exception(
                    f'This time window is not valid: {time_schedule[0][0].time()} to {time_schedule[0][1].time()}')
            for j in range(i + 1, len(time_schedule)):
                if time_schedule[i][1] > time_schedule[j][0]:
                    raise Exception(
                        f'This two time windows have overlaps: {time_schedule[0][0].time()} to {time_schedule[0][1].time()} and {time_schedule[j][0].time()} to {time_schedule[j][1].time()}')

    def run_immediate_irrigation_job(self, duration):
        self.immediate_scheduler.add_job(lambda :actuator_controller.irrigation_controller.run_cycle(duration=duration, nutrient=False))
        print(self.immediate_scheduler.get_jobs())

    def add_irrigation_jobs(self, irrigation_schedule: List, alter=True):
        irrigation_jobs = [
            self.scheduler.add_job(lambda: actuator_controller.irrigation_controller.run_cycle(duration=duration),
                                   'cron',
                                   id=f'IRG-{irrigation_time.time()}', hour=irrigation_time.hour,
                                   minute=irrigation_time.minute) for
            irrigation_time, duration in irrigation_schedule]
        if alter:
            conn = sqlite.get_database_connection()
            [sqlite.insert_irrigation_schedule_with_datetime(conn=conn, start_datetime=irrigation_time, duration=duration) for
            irrigation_time, duration in irrigation_schedule]
            self.load_irrigation_schedule(conn) 


        return irrigation_jobs

    def add_air_jobs(self, air_schedule, alter=True):
        if alter:
            self.valid_schedule(time_schedule=self.air_schedule + air_schedule)
        air_on_jobs = [
            self.scheduler.add_job(actuator_controller.air_controller.on, 'cron', hour=air_on_time.hour,
                                   id=f'FAN-ON-{air_on_time.time()}',
                                   minute=air_on_time.minute)
            for air_on_time, air_off_time in air_schedule
        ]
        air_off_jobs = [
            self.scheduler.add_job(actuator_controller.air_controller.off, 'cron', hour=air_off_time.hour,
                                   id=f'FAN-OFF-{air_off_time.time()}',
                                   minute=air_off_time.minute)
            for air_on_time, air_off_time in air_schedule
        ]
        if alter:
            with sqlite.get_database_connection() as conn:
                [sqlite.insert_air_schedule_with_datetime(conn=conn, start_datetime=start_time, end_datetime=end_time) for
                start_time, end_time in air_schedule]
                self.load_air_schedule(conn=conn)
        return air_on_jobs + air_off_jobs

    def add_lighting_jobs(self, lighting_schedule, alter=True):
        if alter:
            self.valid_schedule(time_schedule=self.lighting_schedule + lighting_schedule)

        lighting_on_jobs = [
            self.scheduler.add_job(actuator_controller.led_controller.power_on, 'cron',
                                   id=f'LIGHT-ON-{lighting_on_time.time()}',
                                   hour=lighting_on_time.hour, minute=lighting_on_time.minute) for
            lighting_on_time, lighting_off_time in lighting_schedule]
        lighting_off_jobs = [
            self.scheduler.add_job(actuator_controller.led_controller.power_off, 'cron',
                                   id=f'LIGHT-OFF-{lighting_off_time.time()}',
                                   hour=lighting_off_time.hour, minute=lighting_off_time.minute) for
            lighting_on_time, lighting_off_time in lighting_schedule]

        if alter:
            with sqlite.get_database_connection() as conn:
                [sqlite.insert_lighting_schedule_with_datetime(conn=conn, start_datetime=start_time, end_datetime=end_time) for
                start_time, end_time in lighting_schedule]
                self.load_lighting_schedule(conn=conn)
        return lighting_on_jobs + lighting_off_jobs

    def remove_irrigation_job(self, scheduled_time):

        try:


            with  sqlite.get_database_connection() as conn:
                job_id = f'IRG-{scheduled_time}'
                self.scheduler.remove_job(job_id)
                sqlite.remove_irrigation_schedule(conn=conn, start_time=scheduled_time)
                self.load_irrigation_schedule(conn=conn)

            if self.status:
                self.reinitiate_state()

        except Exception as e:
            logging.error(e)
            raise e

    def remove_window_jobs(self, scheduled_window, job_type):
            try:    
                on_time, off_time = scheduled_window.split('-')
                
                on_id = f'{job_type}-ON-{on_time}'
                off_id = f'{job_type}-OFF-{off_time}'

                self.scheduler.remove_job(on_id)
                self.scheduler.remove_job(off_id)
                if job_type == 'LIGHT':
                    with  sqlite.get_database_connection() as conn:
                        sqlite.remove_lighting_schedule(conn=conn, start_time=on_time, end_time=off_time)
                        self.load_lighting_schedule(conn=conn)

                elif job_type == 'AIR':
                    with  sqlite.get_database_connection() as conn:
                        sqlite.remove_air_schedule(conn=conn, start_time=on_time, end_time=off_time)
                        self.load_air_schedule(conn=conn)
                    
                
                if self.status:
                    self.reinitiate_state()
            except Exception as e:
                logging.error(e)
                raise e
        

    def start(self):
        if not self.status:
            self.reinitiate_state()
            self.scheduler.start() if not self.initiated else self.scheduler.resume()
            self.status = True
            self.initiated = True

    def pause(self):
        if self.status:
            self.scheduler.pause()
            self.turn_off_actuators()
            self.status = False


actuator_scheduler = ActuatorScheduler()
