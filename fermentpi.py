import json
import requests
from w1thermsensor import W1ThermSensor
import os
import socket
import time


test = False
configFileName = "fermentpi.config"
tickIntervalSec = 10

def getControllerName():
    return socket.gethostname()

def getSensorsTemp():
    print("Getting temp")
    if test:
        result = [{'Address':"123456", 'CurrentValue':23.5}, {'Address':"123457", 'CurrentValue':24.5}]
    else:    
        result = []
        for sensor in W1ThermSensor.get_available_sensors():
            result.append({sensor.id, sensor.get_temperature()})
    print(result)
    return result
    
def readConfig():
    print("Reading config")
    print(configFileName)
    config = {
            'ControllerName':getControllerName(),
            'ServerURL':'http://162.243.82.40:3000/api/Controllers/report',
            'Sensors' : []
        }
    configFile = False
    try:
        configFile = open(configFileName, "r")
        config = json.load(configFile)
    except:
        print("cannot open config file")
    finally:
        if configFile:
            configFile.close()
    return config
        
def saveConfig(config):
    print("Saving config:")
    print(configFileName)
    try:
        configFile = open(configFileName, "w")
        json.dump(config, configFile,sort_keys=True,
                  indent=4, separators=(',', ': '))
    except e:
        print(e)
    finally:
        configFile.close()
    
def doReport(config, temp):
    print("Reporting status:")
    print(config)
    print(temp)
    try:
        config['Sensors'] = temp
        data={"controllerStatus":json.dumps(config)}
        url = config['ServerURL']
        headers = {'accept':'application/json'}
        response = requests.post(url, data, headers=headers, timeout=10)
        result = response.json()
        if result:
            config = result['controllerStatus']
            print("New config: ")
            print(config)
    except:
        print("Request error")
    finally:
        return config
    
def doControl(config, temp):
    return

def main():
    config = readConfig()
    while True:
        temp = getSensorsTemp()
        config = doReport(config, temp)
        saveConfig(config)
        doControl(config, temp)
        print("===================== Sleeping ===========================")
        time.sleep(tickIntervalSec)
    
if __name__ == '__main__':
    main()

