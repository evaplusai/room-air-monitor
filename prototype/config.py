
VC = 5.0  # Circuit voltage
AR_MAX = 1023.0  # Maximum output value of the analogRead method

NB_R0_READ = 50  # number of readings to average R0 value
R0_INTERVAL = 0.5  # number of seconds between each reading for R0
NB_RS_READ = 5  # number of readings for the sensor value
RS_INTERVAL = 0.05  # number of seconds between each reading for Rs

MQ_SENSORS = {
    'mq2': {
        'pin': 0,
        'r0_rs_air': 9.48,
        'r0': 5.29008438819 # replace with calibration 
    },
    'mq9': {
        'pin': 1,
        'r0_rs_air': 9.74,
        'r0': 7.97662296636 # replace with calibration 
    },
    'mq5': {
        'pin': 2,
        'r0_rs_air': 6.45,
        'r0': 2.28503279666 # replace with calibration 
    }
}

CURVES = {
    'mq2': {
        'co': {
            'x': 2.3,
            'y': 0.72,
            'slope': -0.34
        },
        'smoke': {
            'x': 2.3,
            'y': 0.53,
            'slope': -0.44
        },
        'ch4': {
            'x': 2.3,
            'y': 0.49,
            'slope': -0.38
        },
        'alcohol': {
            'x': 2.3,
            'y': 0.45,
            'slope': -0.37
        },
        'h2': {
            'x': 2.3,
            'y': 0.32,
            'slope': -0.47
        },
        'propane': {
            'x': 2.3,
            'y': 0.23,
            'slope': -0.46
        },
        'lpg': {
            'x': 2.3,
            'y': 0.21,
            'slope': -0.47
        }
    },
    'mq5': {
        'co': {
            'x': 2.3,
            'y': 0.59,
            'slope': -0.13
        },
        'alcohol': {
            'x': 2.3,
            'y': 0.55,
            'slope': -0.23
        },

        'h2': {
            'x': 2.3,
            'y': 0.24,
            'slope': -0.25
        },
        'ch4': {
            'x': 2.3,
            'y': -0.02,
            'slope': -0.4
        },
        'lpg': {
            'x': 2.3,
            'y': -0.15,
            'slope': -0.41
        }
    },
    'mq9': {
        'ch4': {
            'x': 2.3,
            'y': 0.49,
            'slope': -0.38
        },
        'lpg': {
            'x': 2.3,
            'y': 0.31,
            'slope': -0.47
        },
        'co': {
            'x': 2.3,
            'y': 0.21,
            'slope': -0.44
        }
    }
}
