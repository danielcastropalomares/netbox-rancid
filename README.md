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
