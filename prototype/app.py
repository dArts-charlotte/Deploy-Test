import logging
from datetime import datetime 
from flask import Flask, render_template, redirect, request
from models.sensors.sensor_scheduler import sensor_scheduler
from models.actuators.actuator_scheduler import actuator_scheduler

from models.actuators.actuator_repository import actuator_repository

app = Flask(__name__)


@app.route("/")
def index():
    scheduler_status = actuator_scheduler.status
    irrigation_schedule = [cycle_time.time() for cycle_time in actuator_scheduler.irrigation_schedule]
    lighting_schedule = [(lighting_on.time(),lighting_off.time()) for lighting_on, lighting_off in actuator_scheduler.lighting_schedule] 
    air_schedule = [(air_on.time(), air_off.time()) for air_on, air_off in actuator_scheduler.air_schedule] 
    return render_template('index.html', scheduler_status=scheduler_status, irrigation_schedule=irrigation_schedule, lighting_schedule=lighting_schedule, air_schedule=air_schedule)


@app.route("/scheduler/on")
def start_scheduler():
    sensor_scheduler.start()
    actuator_scheduler.start()
    return redirect("/")


@app.route("/scheduler/off")
def stop_scheduler():
    sensor_scheduler.pause()
    actuator_scheduler.pause()
    return redirect("/")

@app.route("/light/on")
def lights_on():
    actuator_repository.main_led.on()
    return redirect("/")

@app.route("/light/off")
def lights_off():
    actuator_repository.main_led.off()
    return redirect("/")

@app.route("/fans/on")
def fans_on():
    actuator_repository.fans_on()
    return redirect("/")

@app.route("/fans/off")
def fans_off():
    actuator_repository.fans_off()
    return redirect("/") 

@app.route("/irg/run")
def run_water_cycle():
    actuator_repository.run_water_cycle()
    return redirect("/")

@app.route("/remove/<type>/<time>")
def remove_time(type, time):
    if type == "IRG":
        actuator_scheduler.remove_irrigation_job(scheduled_time=time)
    else:
        actuator_scheduler.remove_window_jobs(scheduled_window=time, job_type=type)
    if actuator_scheduler.status:
        actuator_scheduler.initial_state()
    return redirect("/")


@app.route("/add/", methods=["POST"])
def add_time():
    job_type = request.form['type']
    try:
        
        if job_type == 'IRG':
            job_time = request.form['time']
            job_datetime = datetime.strptime(job_time, "%H:%M")
            actuator_scheduler.create_irrigation_jobs([job_datetime])
        else:
            on_datetime = datetime.strptime(request.form['from'], "%H:%M")
            off_datetime = datetime.strptime(request.form['to'], "%H:%M")

            if job_type == 'LIGHT':
                actuator_scheduler.create_lighting_jobs([(on_datetime, off_datetime)])
            else:
                actuator_scheduler.create_air_jobs([(on_datetime, off_datetime)])
        if actuator_scheduler.status:
            actuator_scheduler.initial_state()

    except Exception as e:
        logging.error(e)

    
    return redirect("/")

if __name__ == '__main__':
    app.debug = True
    app.run()