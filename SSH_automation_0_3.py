#Automation Station by Jamous Bitrick
#version: BETA 0.3 7/13/22

#Imports
from multiprocessing.pool import ThreadPool
import paramiko
import getpass
import time

#Functions
def sshConnect(address):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=address,username=username,password=password,allow_agent=False)

        print ("Successful connection", address)

        remote_connection = ssh_client.invoke_shell()

        commandList = open (commands)
        for lines in commandList:
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
    
    except:
        print("There was an exception on host " + address + "\nWriting host ip address to exceptions.txt")
        exceptionFile = open("exceptions.txt", 'a')
        exceptionFile.write("There was an exception on host " + address + "\n")



#Get output file, username, and password
print("... \nWelcome to the SSH automation script. \nYou will be prompted for a lists of hosts, list of commands, usernae, and password. \nAll files must be in the same directory as this script. \nNone of these variables are ever stored.")
hosts = input("List of hosts (Ex. hosts.txt): ")
commands = input("List of commands (Ex. commands.txt): ")
outputFile = input("Name of log file (Ex. output.txt): ")
username = input("Username: ")
password = getpass.getpass()

#Define number of threads
#threads = Pool(8)

#Open list of clients and read into all_ip_addresses
hostList = open (hosts)
all_ip_addresses = []
for line in hostList:
    try: 
        ip_address = line.strip()
        all_ip_addresses.append(ip_address)
    except:
        print("Could not read from file " + hostList + "\nWriting error to error.txt")
        exceptionFile = open("error.txt", 'a')
        exceptionFile.write("Could not read from file " + hostList + "\n")

#Create multiple threads and try to connect
thread = ThreadPool(100)
thread.map(sshConnect, all_ip_addresses)
thread.close()
thread.join()