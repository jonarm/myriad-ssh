# myriad-ssh #
==============
Python script that connects to multiple servers via ssh to execute commands and generate a report

## Requirements ##
------------------
* Paramiko

## Usage ##
-----------
1. Run the script
```
/myriad-ssh.py
```
2. Enter the necessary details
```
Enter username: _uname_
Password: _pass_
Enter the remote command: date && uname -a
Enter the serverlist file:/home/uname/serverlistfile
```
Note: Server list file contains the server hostnames/IP written in one column
3. Progress and Output
```
Total number of servers: 5
Progress: 80%............Done
```
Output file: myriad-ssh-log.csv
