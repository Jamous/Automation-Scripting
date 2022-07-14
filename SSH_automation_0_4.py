#Automation Station by Jamous Bitrick
#version: BETA 0.4 7/14/22

#Imports
from msilib.schema import Error
from multiprocessing.pool import ThreadPool
import paramiko
import getpass
import time
import re

#Functions
def sshConnect(address):
    
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=address,username=username,password=password,allow_agent=False)

        print ("Successful connection", address)
        
        #Send to SSH commands. 
        sshCommandsList(ssh_client)

        time.sleep(1)
        ssh_client.close
    
    except Exception as exc:
        print("There was an exception on host " + address + "\n" + str(exc) + "\nWriting host ip address to exceptions.txt")
        exceptionFile = open("exceptions.txt", 'a')
        exceptionFile.write("There was an exception on host " + address + "\n" + str(exc) + "\n\n")

#You can create your own method here for each type of task.

#sshComandsList is for inputs from file. Ex input.txt
def sshCommandsList(ssh_client_cmd):
        remote_connection = ssh_client_cmd.invoke_shell()
        remote_connection.send("ls -l\n")

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

#sshComands is for indivual inputs
def sshCommands(ssh_client_cmd): 
        remote_connection = ssh_client_cmd.invoke_shell()
        remote_connection.send("ls -l\n")

        time.sleep(1)
        output = remote_connection.recv(65535)
        printableOutput = output.decode('utf-8')
        print(printableOutput)

        outfile = open(outputFile, 'a')
        outfile.write(printableOutput)

#sshReadCiscoIntStats
def sshIfElseCommands(ssh_client_cmd): 
        remote_connection = ssh_client_cmd.invoke_shell()
        remote_connection.send("show int\n                                                                                       ")

        #match for line protocol is


        time.sleep(1)
        output = remote_connection.recv(65535)
        printableOutput = output.decode('utf-8')
        #print(printableOutput)

        match_clause = {'line', 'minute'}
        stripped_chars = ',."\'|'

        for line in printableOutput.splitlines():
            lst = line.lower().split()
            stripped_and_lower = {word.strip(stripped_chars) for word in lst}
            if stripped_and_lower & match_clause:
                print(line)

        outfile = open(outputFile, 'a')
        outfile.write(printableOutput)

#Main function
#Get output file, username, and password
print("... \nWelcome to the SSH automation script. \nYou will need a lists of hosts (hosts.txt), list of commands (commands.txt), username, and password. \nAll files must be in the same directory as this script.")

#Ask user if custom values will be used.
while True:
    try:
        customVal = input("Use custom host and command files? (default is hosts.txt and commands.txt) y or n :")
        if (customVal == "y") or (customVal == "n"):
            break
        else:
            raise ValueError
    except ValueError:
        print("You must input y or n. Please try again.")

#Get inputs
if customVal == "y":
    hosts = input("List of hosts (Ex. hosts.txt): ")
    commands = input("List of commands (Ex. commands.txt): ")
    outputFile = input("Name of log file (Ex. output.txt): ")
elif customVal == "n":
    print("List of hosts: hosts.txt \nList of commands: commands.txt \nName of log file: output.txt")
    hosts = "hosts.txt"
    commands = "commands.txt"
    outputFile = "output.txt"

username = input("Username: ")
password = getpass.getpass()

#Open list of clients and read into all_ip_addresses. Ignore empty lines.
hostList = open (hosts)
all_ip_addresses = []
for line in hostList:
    try: 
        ip_address = line.strip()
        if ip_address != "":
            all_ip_addresses.append(ip_address)
    except Exception as exc:
        print("Could not read from file " + hostList + "\n" + str(exc) + "\nWriting error to error.txt")
        exceptionFile = open("error.txt", 'a')
        exceptionFile.write("Could not read from file " + hostList + "\n" + str(exc) + "\n\n")

#Create multiple threads and try to connect
thread = ThreadPool(100)
thread.map(sshConnect, all_ip_addresses)
thread.close()
thread.join()


#Changelog
'''
v0.4
Error handling now reports errors
Paramiko does not try and connect to emtpy lines
Threads is now set to 100
SSH commands are now in their own method. Change commands in this method. New methods can be created. Ex. def sshCommands(ssh_client_cmd)
Opperator is prompted to use default peramaters of commands.txt, hosts.txt, and output.txt or to use custom peramaters.
'''