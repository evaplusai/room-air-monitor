import grovepi
import time

MQ_SENSORS = {
    'mq2': {
        'pin': 0,
        'r0_rs_air': 9.48 
    },

    'mq9': {
        'pin': 1,
        'r0_rs_air': 9.74
    },

    'mq5': {
        'pin': 2,
        'r0_rs_air': 6.45
    }
}

 

NB_R0_READ = 50  # number of readings to average R0 value
R0_INTERVAL = 0.5  # number of seconds between each reading for R0
NB_RS_READ = 5  # number of readings for the sensor value
VC = 5.0  # Circuit voltage
AR_MAX = 1023.0  # Maximum output value of the analogRead method

mq_values = {}

for sensor, data in MQ_SENSORS.items():
    grovepi.pinMode(data['pin'],"INPUT")
    mq_values[sensor] = 0  
    

for i in range(NB_R0_READ):
    for sensor, value in mq_values.items():
        mq_values[sensor] += grovepi.analogRead(MQ_SENSORS[sensor]['pin'])

    time.sleep(R0_INTERVAL)


for sensor, value in mq_values.items():
   
    # average sensor value
    mq_values[sensor] = mq_values[sensor]/NB_R0_READ   
   

    # sensor voltage
    mq_values[sensor] = (mq_values[sensor]/AR_MAX) * VC    
    

    # sensor resistance
    mq_values[sensor] = (VC - mq_values[sensor])/mq_values[sensor]

    # R0 value
    mq_values[sensor] = mq_values[sensor]/MQ_SENSORS[sensor]['r0_rs_air']

    print('R0 value for sensor {}: {}'.format(sensor, mq_values[sensor]))
    
#R0 value for sensor mq9: 7.97662296636
#R0 value for sensor mq2: 5.29008438819
#R0 value for sensor mq5: 2.28503279666
