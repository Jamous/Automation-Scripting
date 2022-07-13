# Automation-Scripting
This is an SSH automation script developed by Jamous Bitrick for Biz Net Technologies Inc.
This script accepts an input of Hosts and commands in two sepreate line-delimited text files. It also accepts and securely stores a login username and password for the duration the script is running.
This script will open an SSH connection to each host and input the commands in the commands file.


 ***Version 0.3***
 
Version 0.3 support multithreading. Python supports over 1000 threads at a time. I have the thread count set to 50. This can be increased to accomodate more concurrent hosts.
