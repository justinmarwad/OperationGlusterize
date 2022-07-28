import threading, paramiko


def deployVMs(gluster_command, hostIP, hostUsername, password, port):
    try:

        ## Connect to user
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostIP, username=hostUsername, password=password, port=port)

        ## Comment Out  ##
        print(f"[+] Commenting out '/home' on {hostIP}:/etc/fstab")        
        stdin, stdout, stderr = client.exec_command(f"sudo cp /etc/fstab /etc/fstab.bak")
        stdin, stdout, stderr = client.exec_command(f"sudo sed -e '/home/ s/^#*/#/' -i /etc/fstab")

        for line in stdout:
            print(line.strip('\n'))
        for line in stderr:
            print(line.strip('\n'))

        ## Add Gluster  ##
        print(f"[+] Adding Gluster command on {hostIP}:/etc/fstab")        
        stdin, stdout, stderr = client.exec_command(f"echo '{gluster_command}' | sudo tee -a /etc/fstab")

        for line in stdout:
            print(line.strip('\n'))
        for line in stderr:
            print(line.strip('\n'))

        client.close()

    finally:
        if client:
            client.close()
    


username = "username"
password = "password"
port = 22

gluster_command = "localhost:/vol01/desktops/home /home glusterfs defaults,_netdev                   0       0"

IPs = []
ipSourceList = open('deploymentTargets.txt', 'r')
targets = ipSourceList.readlines()


for ip in targets:
    IPs.append(ip.strip())

print(IPs)

for host in IPs:
    thread = threading.Thread(target=deployVMs, args=(gluster_command, host, username, password, port, ))
    thread.start()


