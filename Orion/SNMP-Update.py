import requests
from orionsdk import SwisClient
import ast
import sys

# Define some constant variables

EngineIDnew = 3
username = "______________"
password = "______________"
npm_server = '<orionServerFQDN>'

swis = SwisClient(npm_server, username, password)
requests.packages.urllib3.disable_warnings()


# Count number of lines

DeviceList = open("devices.txt", "r")
LineCount = len(DeviceList.readlines())
DeviceList.close()


# Reopen the file for processing

DeviceList = open("devices.txt", "r")
Counter = 0


# Iterate through the file

while Counter < LineCount:

    NodeID = int(DeviceList.readline().rstrip())
    
    print("Processing: %d" %NodeID)

    # Initiate query and provide prefered result

    URI = ('swis://<orionServerFQDN>/Orion/Orion.Nodes/NodeID=%d' %NodeID)
    results_dict = swis.read(URI)
    
    print("Here is the before result: %d, %s, %d, %d" %(results_dict['NodeID'], results_dict['NodeName'], results_dict['EngineID'], results_dict['Status']))
    
    swis.update(URI, EngineID=EngineIDnew)
    NodePoll = ('N:%d' %NodeID)
    swis.invoke('Orion.Nodes', 'PollNow', NodePoll)
    #print("\n")

    results_dict = swis.read('swis://<orionServerFQDN>/Orion/Orion.Nodes/NodeID=%d' %NodeID)
    print("Here is the after result: %d, %s, %d, %d" %(results_dict['NodeID'], results_dict['NodeName'], results_dict['EngineID'], results_dict['Status']))
    print("\n================================================\n")
    Counter += 1

DeviceList.close()
