# network_testing-server

# Introduction
The project is organized and developed in order to be deployed over grid5000 (for further information : https://www.grid5000.fr/mediawiki/index.php/Grid5000:Home)
Some choices have been made to render the experimentation scripts compliant with Grid5000's tools.

However, you can build your own image and deploy it on other computers grid (a tutorial will explain in details the deployment process and will be the purpose of a future work)
If you want to see the progress of the project, you can consult the TODO file.
Don't hesitate to bring your contributions, I'll be happy to integrate them into the project

# How to build image

```bash
# In the project folder
docker build -t name_of_your_image .
docker run -it name_of_your_image /bin/bash
```
Open new terminal (don't close the first one and keep the container running)

Inside the new terminal :
```bash
# Get the containerID
docker ps
# Copy the containerID (of the right container and past it in the next command line instead of containerID)
docker export containerID > your_image_name.tar
gzip your_image_name.tar
```

## How to deploy images on Grid5000
This part explains how to test server image deployed in virtual node over Grid5000. If you want to launch the entire experimentation and run client script properly, consult the README of quentinl-c/network-testing.

Physical nodes reservation :
```bash
# Reserve two nodes (you can reserve as many as you want but at least two)
oarsub -t deploy -l slash_22=1+nodes=2 -I
# Install Jessie distribution on nodes
kadeploy3 -f $OAR_NODE_FILE -e jessie-x64-nfs -k
# Install distem on nodes
distem-bootstrap
```

Deployment with distem :
```bash
# Connection to the coordinator (indicated by distem-bootstrap command output) as root
ssh root@coordinator-node
# On the coordinator
distem --create-vnetwork vnetwork=vnetwork,address=10.144.0.0/22
distem --create-vnode vnode=node-1,pnode=physical-node-name,rootfs=file:///home/qlaportechabasse/public/server-lxc.tar.gz,sshprivkey=/root/.ssh/id_rsa,sshpubkey=/root/.ssh/id_rsa.pub
distem --create-viface vnode=node-1,iface=if0,vnetwork=vnetwork
distem --start-vnode node-1
# Connection to the vnode
ssh vnode_ip
# On the vnode
# Specify the gateway
ifconfig if0 vnode_ip netmask 255.252.0.0
route add default gw 10.147.255.254 dev if0 # Be careful, 10.147.255.254 is the gateway of Nancy site, you must change it if you are on another site
# Add the right DNS configuration
rm /etc/resolv.conf
cp /home/resolv.conf /etc/
# Add localhost into hosts file
echo "127.0.0.1 localhost" >> /etc/hosts
```

Afterward you have to give the configuration of the experimentation either passing information by environment variables :

```bash
export SERVER_ADDRESS='SERVER_ADDRESS' &&
export RABBITMQ_ADDRESS='RABBITMQ_ADDRESS' &&
export TARGET='TARGET' &&
export WRITERS=42 &&
export READERS=9 &&
export TYPING_SPEED=10 &&
export DURATION=12000 &&
# And run server
/opt/www/__init__.py -e
```

Or giving configuration with a JSON file :

```JSON
{
  "exp_name" : "Exp name",
  "writers" : 3,
  "readers": 1,
  "typing_speed" : 2,
  "duration" : 30,
  "target": "http://target.com"
}
```

```bash
/opt/www/__init__.py -f path/to/config/file.json
```
### Useful links :

* Distem tutorial : http://distem.gforge.inria.fr/tutorial.html
* Distem FAQ : http://distem.gforge.inria.fr/faq.html
* Distem Documentation : http://distem.gforge.inria.fr/documentation.html

# Deployment on the cloud (anywhere)
TODO
