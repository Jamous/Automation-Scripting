# Automation-Scripting
This is an SSH automation script developed by Jamous Bitrick for Biz Net Technologies Inc.
This script accepts an input of Hosts and commands in two sepreate line-delimited text files. It also accepts and securely stores a login username and password for the duration the script is running.
This script will open an SSH connection to each host and input the commands in the commands file.

***Version Beta 0.5***
* Threadpool now creates num threads equal to number of ip addresses
* Moved from Paramiko to Netmiko for faster support and extended features.


***Version Beta 0.4***
* Error handling now reports errors
* Paramiko does not try and connect to emtpy lines
* Threads is now set to 100
* SSH commands are now in their own method. Change commands in this method. New methods can be created. Ex. def sshCommands(ssh_client_cmd)
* Opperator is prompted to use default peramaters of commands.txt, hosts.txt, and output.txt or to use custom peramaters.


 ***Version Beta 0.3***
 
Version Beta 0.3 supports multithreading. Python supports over 1000 threads at a time. I have the thread count set to 50. This can be increased to accomodate more concurrent hosts.
