import requests
from orionsdk import SwisClient
import getpass

def main():
    npm_server = '<orionServerFQDN>'
    username = input("What is your username? (e.g. domain\...")
    password = getpass.getpass("What is your password? ")

    swis = SwisClient(npm_server, username, password)
    print("Custom Property Update Test:")
    results = swis.query(
        "SELECT Uri FROM Orion.Nodes WHERE NodeID=@id",
        id=4192)  # set valid NodeID!
    print(results)
    uri = results['results'][0]['Uri']
    print(uri)
    swis.update(uri + '/CustomProperties', Workspace='Production', Department='Server Team')
    obj = swis.read(uri + '/CustomProperties')
    print (obj)


requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()
