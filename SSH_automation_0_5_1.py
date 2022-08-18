#Automation Station by Jamous Bitrick
#version: BETA 0.5.1 8/18/22
#https://github.com/Jamous/Automation-Scripting
''' List of Methods
sshConnect: Used to initiate connections to hosts
sshCommandsList: Used to communicate with hosts. Make adjustments to this method 
regexSearch: Used for regex searching. Can be combined with conditional if/else statements.
main: No actual method, this approximates global variables
'''
#Imports
from msilib.schema import Error
from multiprocessing.pool import ThreadPool
import getpass
import re
from netmiko import ConnectHandler

#ssh dictionary device types. You must select a corosponding device type for the dictionary
#deviceType = 'cisco_ios' #Cisco IOS SSH devices
deviceType = 'ubiquiti_edgeswitch' #Ubiquiti Edge Switch SSH devices
#deviceType = 'ubiquiti_edgerouter' #Ubiquiti Edge Router SSH devices

#Functions
def sshConnect(address):
    try:
        sshDictionary = {
            'device_type': deviceType,
            'host':   address,
            'username': username,
            'password': password,
        }

        net_connect = ConnectHandler(**sshDictionary)
        
        #Send to SSH commands. 
        print ("Successful connection", address)
        sshCommandsList(net_connect)

    except Exception as exc:
        print("There was an exception on host " + address + "\n" + str(exc) + "\nWriting host ip address to exceptions.txt")
        exceptionFile = open("exceptions.txt", 'a')
        exceptionFile.write("There was an exception on host " + address + "\n" + str(exc) + "\n\n")

def sshCommandsList(net_connect):
    printableOutput = ""

    commandList = open (commands)
    for lines in commandList:
        command = lines.strip()
        commandOut = net_connect.send_command(command)
        printableOutput += commandOut

    print(printableOutput)
    outfile = open(outputFile, 'a')
    outfile.write(printableOutput)

#Pass two values to regexSearch. A string to be parsed, and an expression to be matched. If the expression is in the string, this method will return a boolean vlaue of true.
def regexSearch(strIn,expression):
    boolVal = bool(re.search(expression,strIn))
    return boolVal

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
thread = ThreadPool(len(all_ip_addresses))
thread.map(sshConnect, all_ip_addresses)
thread.close()
thread.join()