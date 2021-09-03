#Automation Station by Jamous Bitrick
#version: BETA 0.1 9/3/21

#Imports
import paramiko
import getpass
import time

#Get output file, username, and password
print("... \nWelcome to the SSH automation script. \nYou will be prompted for a lists of hosts, list of commands, usernae, and password. \nAll files must be in the same directory as this script. \nNone of these variables are ever stored.")
hosts = input("List of hosts (Ex. hosts.txt): ")
comands = input("List of comands (Ex. comands.txt): ")
outputFile = input("Name of log file (Ex. output.txt): ")
username = input("Username: ")
password = getpass.getpass()

#Open list of clients
hostList = open (hosts)

#read each line in F and open a connection
for line in hostList:
    ip_address = line.strip()

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address,username=username,password=password,allow_agent=False)

    print ("Successful connection", ip_address)

    remote_connection = ssh_client.invoke_shell()

    comandList = open (comands)
    for lines in comandList:
        comand = lines.strip()
        remote_connection.send(comand + "\n")
        time.sleep(2)

    time.sleep(1)
    output = remote_connection.recv(65535)
    printableOutput = output.decode('utf-8')
    print(printableOutput)

    outfile = open(outputFile, 'a')
    outfile.write(printableOutput)

    time.sleep(1)
    ssh_client.close
