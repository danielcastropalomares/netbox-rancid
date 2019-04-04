# netbox-rancid
Sync devices from Netbox to rancid

# Netbox

## Create token

Create a new token:

![Screenshot](images/01.png)
![Screenshot](images/02.png)

## Create new key

we need a private an public key for en encrypt and decrypt passwords:

![Screenshot](images/03.png)

![Screenshot](images/04.png)

## Custom field Rancid

![Screenshot](images/05.png)


# Rancid

We need create the .cloginrc and routerdb:

	https://github.com/danielcastropalomares/ansible-container-rancid
  
Install the python script inside of the machine rancid:

	/var/lib/rancid/netbox-sync.py
  
Modify the variables inside of script:

	####VARIABLES#####
	url = "http://localhost:32769"
	token = "Token 0123456789abcdef0123456789abcdef01234567"
	cloginRancid = "/var/lib/rancid/.cloginrc"
	routerdbRancid = "/var/lib/rancid/routers/router.db"
	apiBaseDevice = url + "/api/dcim/devices/?cf_rancid=1&status=1"
	apiBaseSecret = url + "/api/secrets/secrets/?device_id="
	pathKeyRsa = "/var/lib/rancid/key/rsa"
	###################

Download the private key from netbox:

	/var/lib/rancid/key/rsa
