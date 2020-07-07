import numpy as np
import time
import sys
from datetime import datetime
from pathlib import Path
import config as cfg
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


import grovepi  


try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from sgp30 import SGP30

def get_ppm(Rs_R0_ratio, curve):
    #Calculate the corresponding ppm value for a rs_ro_ratio 
    x_val = (np.log10(Rs_R0_ratio) - curve['y'])/curve['slope'] + curve['x']
    ppm_val = np.power(x_val, 10)
    return ppm_val

# Initialize Firebase 
firebase_path = Path.cwd() / cfg.FIREBASE_CREDS_JSON
cred = credentials.Certificate(str(firebase_path))
firebase_admin.initialize_app(cred)

db = firestore.client()

mq_values = {}
ppm_values = {}


for mq_sensor, data in cfg.MQ_SENSORS.items():

    grovepi.pinMode(data['pin'],"INPUT")
    mq_values[mq_sensor] = 0  

    for gas, curve in cfg.CURVES[mq_sensor].items():
        ppm_values[mq_sensor] = {} 


# Sensor BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
bme280.setup(mode="forced")

sgp30 = SGP30()
print("SGP30 Sensor warming up, please wait...")
def crude_progress_bar():
    sys.stdout.write('.')
    sys.stdout.flush()

sgp30.start_measurement(crude_progress_bar)
sys.stdout.write('\n')

running = True
while running:
    try:
        # get temperature, pressure and humidity with BME280 sensor        
        temperature = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()
        
        sgp_result = sgp30.get_air_quality()
        
        #print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, pressure, humidity))
        
        for i in range(cfg.NB_RS_READ):
            for mq_sensor, value in mq_values.items():
                mq_values[mq_sensor] += grovepi.analogRead(cfg.MQ_SENSORS[mq_sensor]['pin'])
            time.sleep(cfg.RS_INTERVAL)

        
        for mq_sensor, value in mq_values.items():
           
            mq_values[mq_sensor] = mq_values[mq_sensor]/cfg.NB_RS_READ

            mq_values[mq_sensor] = mq_values[mq_sensor]/cfg.AR_MAX * cfg.VC

            mq_values[mq_sensor] = (cfg.VC - mq_values[mq_sensor])/mq_values[mq_sensor]
 
            mq_values[mq_sensor] = mq_values[mq_sensor]/cfg.MQ_SENSORS[mq_sensor]['r0']


            for gas, curve in cfg.CURVES[mq_sensor].items():
                ppm_values[mq_sensor][gas] = get_ppm(mq_values[mq_sensor], curve)


        # save data to Firebase
        sensor_values = {mq_sensor + '_' + gas + '_ppm': ppm
                            for mq_sensor, gases in ppm_values.items()
                            for gas, ppm in gases.items()
                          }
        

        sensor_values['temperature'] = temperature
        sensor_values['pressure'] = pressure
        sensor_values['humidity'] = humidity
        
        sensor_values['equivalent_co2'] = sgp_result.equivalent_co2
        sensor_values['total_voc'] = sgp_result.total_voc

        sensor_values['date'] = datetime.now()

        db.collection(cfg.FIREBASE_DB_NAME).add(sensor_values)  
        
        time.sleep(cfg.FIREBASE_INTERVAL)

    except IOError:
        print ("Error reading MQ data")

    except KeyboardInterrupt:
        print('Program stopped')
        running = False