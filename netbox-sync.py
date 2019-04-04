#!/usr/bin/python
#https://stro.io/netbox-api-integration-with-python-and-powershell/
#https://netbox.readthedocs.io/en/stable/api/working-with-secrets/
import requests
####VARIABLES#####
url = "http://localhost:32769"
token = "Token 0123456789abcdef0123456789abcdef01234567"
cloginRancid = "/home/rancid/var/lib/rancid/.cloginrc"
routerdbRancid = "/home/rancid/var/lib/rancid/routers/router.db"
apiBaseDevice = url + "/api/dcim/devices/?cf_rancid=1&status=1"
apiBaseSecret = url + "/api/secrets/secrets/?device_id="
pathKeyRsa = "/home/rancid/var/lib/rancid/key/rsa"
###################
###Sesion key number for decrypt passwords
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'Authorization': token,
}
keyFile = open(pathKeyRsa, "r")
key = {
    'private_key' : keyFile.read()
}   
url = url + "/api/secrets/get-session-key/"
sessionKey = requests.post(url, headers = headers, data=key).json()
###########HEADERS
headers = {  
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': token,
    'X-Session-Key': sessionKey['session_key'] 
}
########FUNCTIONS
def get_Count():  
    resp = requests.get(apiBaseDevice, headers = headers).json()
    return resp['count']

def get_hostName(countdevice):  
    resp = requests.get(apiBaseDevice, headers = headers).json()
    return resp['results'][countdevice]['name']

def get_hostID(countdevice):  
    resp = requests.get(apiBaseDevice, headers = headers).json()
    return resp['results'][countdevice]['id']

def get_secretUser(id):  
    id2 = str(id)
    resp = requests.get(apiBaseSecret + id2, headers = headers).json()
    return resp['results'][0]['name']

def get_secretPass(id):  
    id2 = str(id)
    resp = requests.get(apiBaseSecret + id2, headers = headers).json()
    #return resp['results'][0]['hash']
    return resp['results'][0]['plaintext']

################
for totalCount in range(get_Count()):
    #########ROUTER.db - check if the device exist 
    lineRouter = get_hostName(totalCount)+";cisco;up"
    if lineRouter in open(routerdbRancid).read():
        print("OK exist in file",get_hostName(totalCount),lineRouter,routerdbRancid)
    else:
        print("ADD to file ",get_hostName(totalCount),lineRouter,routerdbRancid)
        outF = open(routerdbRancid, "a")
        print >>outF, lineRouter 

    #########CLOGINRC - check if the device exist 
    lineClogin = [ 
            "add user "         + get_hostName(totalCount) + " " + get_secretUser(get_hostID(totalCount)),
            "add password "     + get_hostName(totalCount) + " " + get_secretPass(get_hostID(totalCount)),
            "add method "       + get_hostName(totalCount) + " ssh",
            "add autoenable "   + get_hostName(totalCount) + " 1" 
    ]
    for lineRouter in lineClogin:
        if  lineRouter in open(cloginRancid).read():
            print("OK exist in file",get_hostName(totalCount),lineRouter,cloginRancid)
        else:
            #add the router to file cloginrc
            print("ADD to file ",get_hostName(totalCount),lineRouter,cloginRancid)
            outF = open(cloginRancid, "a")
            print >>outF, lineRouter 
            outF.close()
