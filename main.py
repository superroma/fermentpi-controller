import json
import requests

def getControllerName():
    return "brewferm1"

def getSensorsTemp():
    #result = []
    #for sensor in W1ThermSensor.get_available_sensors():
    #    result.append({sensor.id, sensor.get_temperature()})
    result = [{'Address':"123456", 'CurrentValue':23.5}, {'Address':"123457", 'CurrentValue':24.5}]
    return result

def logstr(str):
    print(str)
    
def callRemote(temp):
    controllerStatus = {
            'ControllerName':getControllerName(),
            'Sensors': temp
        }
    data={"controllerStatus":json.dumps(controllerStatus)}
    url = 'http://172.22.5.31:3000/api/Controllers/report'
    headers = {'accept':'application/json'}
    response = requests.post(url, data, headers=headers)
    logstr("response="+response.text)
    result = response.json()
    if result:
        controllerStatus = result['controllerStatus']
        print("new status")
    print(controllerStatus)
    
def main():
    logstr("Started")
    temp = getSensorsTemp()
    logstr(temp)
    callRemote(temp)
    logstr("Finished")
    
if __name__ == '__main__':
    main()

