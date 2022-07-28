# Operation Gluzterize #

This script will SSH into all the IPs you list in the deployTargets.txt file, comment out the "/home" entry in the /etc/fstab file, and add a new entry that will cause the /home directory to be mounted from a GlusterFS setup. 