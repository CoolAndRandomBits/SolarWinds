from __future__ import print_function
import re
import requests
import getpass
from orionsdk import SwisClient


def main():
    npm_server = '<orionServerFQDN>'
    username = input("What is your username? (e.g. domain\...")
    password = getpass.getpass("What is your password? ")
    

    swis = SwisClient(npm_server, username, password)
    print("Add an SNMP v1 node:")

    # fill these in for the node you want to add!
    ip_address = input("What is the IP address of the device? ")
    community = input("what is the SNMP community string? ")

    # set up property bag for the new node
    props = {
        'IPAddress': ip_address,
        'EngineID': 2,
        'ObjectSubType': 'SNMP',
        'SNMPVersion': 1,
        'Community': community
    }

    print("Adding node {}... ".format(props['IPAddress']), end="")
    results = swis.create('Orion.Nodes', **props)
    print("DONE!")

    # extract the nodeID from the result
    nodeid = re.search('(\d+)$', results).group(0)

    pollers_enabled = {
        'N.Status.ICMP.Native': True,
        'N.Status.SNMP.Native': True,
        'N.ResponseTime.ICMP.Native': True,
        'N.ResponseTime.SNMP.Native': True,
        'N.Details.SNMP.Generic': True,
        'N.Uptime.SNMP.Generic': True,
        'N.Cpu.SNMP.HrProcessorLoad': True,
        'N.Memory.SNMP.NetSnmpReal': True,
        'N.AssetInventory.Snmp.Generic': True,
        'N.Topology_Layer3.SNMP.ipNetToMedia': False,
        'N.Routing.SNMP.Ipv4CidrRoutingTable': False
    }

    pollers = []
    for k in pollers_enabled:
        pollers.append(
            {
                'PollerType': k,
                'NetObject': 'N:' + nodeid,
                'NetObjectType': 'N',
                'NetObjectID': nodeid,
                'Enabled': pollers_enabled[k]
            }
        )

    for poller in pollers:
        print("  Adding poller type: {} with status {}... ".format(poller['PollerType'], poller['Enabled']), end="")
        response = swis.create('Orion.Pollers', **poller)
        print("DONE!")

    results = swis.query(
        "SELECT Uri FROM Orion.Nodes WHERE NodeID=@id", id=nodeid)  # set valid NodeID!
    uri = results['results'][0]['Uri']

    swis.update(uri + '/CustomProperties', Workspace='Production', Department='Network Support')
    obj = swis.read(uri + '/CustomProperties')


    PollNode = ('N:%d' %nodeid)
    swis.invoke('Orion.Nodes', 'PollNow', PollNode)



requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()
