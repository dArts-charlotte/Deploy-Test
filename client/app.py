
# import os
# import sys
#  # Modify PATH so we can import files from elsewhere in this repo
# from os.path import dirname, join, abspath
# sys.path.insert(0, abspath(join(dirname(__file__), '..')))


import socketio
import json

# from gpiozero import LED
from time import sleep

# import appConfig as config

# from amps.lightingClass import LedMain
# from amps.Irrigation import Irrigation



# # Config file variable

# server_url = config.serverUrl  # connection server URL

server_url = "http://localhost:3000/"

# gpioLedODMainPwr =  config.gpioLedODMainPwr
# gpioLedPWMMainDim =  config.gpioLedPWMMainDim
# gpioLedPWMSup1Dim = config.gpioLedPWMSupOneDim
# gpioLedPWMSup2Dim= config.gpioLedPWMSupTWoDim
# gpioMainPump =config.gpioMainPump
# gpioWtrPump=config.gpioWtrPump
# gpioTrnsPump=config.gpioTrnsPump
# gpioNutrPump=config.gpioNutrPump
# gpiolvl1Sol=config.gpiolvl1Sol
# gpiolvl2Sol=config.gpiolvl2Sol
# gpiolvl3Sol=config.gpiolvl3Sol
# gpiolvl4Sol=config.gpiolvl4Sol
# gpiolvl5Sol=config.gpiolvl5Sol



# lightingControls = LedMain(gpioPwr = gpioLedODMainPwr , gpioDim = gpioLedPWMMainDim , gpioSupp1 = gpioLedPWMSup1Dim, gpioSupp2 = gpioLedPWMSup2Dim)
# IRGControls =Irrigation(gpioMainPump, gpioWtrPump,gpioTrnsPump, gpioNutrPump,
#                 gpiolvl1Sol, gpiolvl2Sol, gpiolvl3Sol, gpiolvl4Sol, gpiolvl5Sol)


# socket-io connections

sio = socketio.Client()
sio.connect(server_url)


@sio.event
def connect():
    print("I'm connected!")


@sio.on("rangeChanged")
def rangeChanged(data):
    # a json containing controller ids and their values
    dashValues = json.loads(data)
    if dashValues['LEDGrowMainPwr'] == 1:

        lightingControls.on()
        mainDim =dashValues['LEDGrowMain']
        sup1Dim =dashValues['LEDGrowSup1']
        sup2Dim =dashValues['LEDGrowSup2']
        lightingControls.dim(mainDim,sup1Dim,sup2Dim)

    else:
        lightingControls.off()


# def hamid():

#     while temstate:
#         print('hi')
@sio.on("IRG")
def IRGChanged(data):

    # a json containing controller ids and their values

    dashValues = json.loads(data)
    for controlId in dashValues:
        IRGControl=getattr(IRGControls,controlId)
        if dashValues[controlId] == 1:
            IRGControl.on()
        else:
            IRGControl.off()




@sio.on('IRGCycle')
def IRGCycleChanged(data):
    print('hello')
    dashValues = json.loads(data)
    for controlId in dashValues:
        # Water Cycle
        if ((controlId == 'IRGWtrCycle' )and (dashValues['IRGWtrCycle'] != 0 )):
            if( 'IRGWtrCycleTime' in dashValues ):
                IRGControls.waterCycle(int(dashValues['IRGWtrCycleTime']))

            else:

                IRGControls.waterCycle()
        elif ((controlId == 'IRGNutrCycle' )and (dashValues['IRGNutrCycle'] != 0 )):
            if( 'IRGNutrCycleTime' in dashValues ):

                IRGControls.nutrientCycle(int(dashValues['IRGNutrCycleTime']))
            else:

                IRGControls.nutrientCycle()
            # IRGControls.nutrientCycle()

stateStepperL =False
stateStepperR =False

def ARMmoveL():
    print (stateStepperL)
def ARMmoveR():
    print (stateStepperR)




@sio.on('Arm')
def ArmChanged(data):
    dashValues = json.loads(data)
    global stateStepperL
    global stateStepperR
    print(dashValues)
    if('swingArmL' in dashValues):

        stateStepperL = dashValues['swingArmL']


    if('swingArmR' in dashValues):
        stateStepperR = dashValues['swingArmR']


while True:
    while stateStepperL == False:
        print(' runningL')
        sleep(1)
    while stateStepperR == False:
        print(' runningR')
        sleep(1)

    print('not running')
    sleep(1)

    # if (stateStepperL):
    #     print('running L')
    #     sleep(1)
    # elif(stateStepperR):
    #     print('running R')
    #     sleep(1)


