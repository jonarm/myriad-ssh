#!/usr/bin/python -tt

# myriad-ssh connects to different servers based on the list given
# and dumps an output based on the executed remote commands.
# Copyright: (c) 2014 Jonar Marzan.
# License: BSD, see LICENSE for more details.



import sys
import socket
import re
import paramiko
import getpass

logFile = 'myriad-ssh-log.csv'


def get_user_info():
    """Obtain accoount details and remote command through user input"""
    user = raw_input('Enter username: ')
    if len(user) == 0 or user.isspace():
       sys.exit('Error: Emtpy username')
    passwd = getpass.getpass('Password: ')
    cmd = raw_input('Enter the remote command: ')
    if len(cmd) == 0 or cmd.isspace():
       sys.exit('Error: Empty command')
    cmd = 'hostname' + ' ' + '&&' + ' ' + cmd #Adds the server hostname in the output file
    return (user,passwd,cmd)


def get_serverlist():
    """Obtain hostname listed on serverlist file through user input"""
    serverlist = raw_input('Enter the serverlist file: ')
    try:
        f = open(serverlist)
    except IOError:
        sys.exit('IOError: No such file or directory. Check also the file permissions')
    servers = f.readlines()
    servercount = len(servers)
    for host in servers:
        return (host,servers,servercount)


def logger_cmd(stdout,stderr):
    """Print the ssh command logs into an output file"""
    try:
        f = open(logFile, 'a')
        print >> f, stdout.readlines(), ',', stderr.readlines()
        f.close()
    except IOError:
        sys.exit('IOError: No such file or directory. Check also the file permissions')


def logger_gen(output):
    """Accepts one argument and logs to the output file"""
    try:
        f = open(logFile, 'a')
        print >> f, output
        f.close()
    except IOError:
        sys.exit('IOError: No such file or directory. Check also the file permissions')


def logger_format():
    """Format the output file by removing unnecessary characters and retaining comma"""
    try:
        f = open(logFile, 'r')
        lines = f.readlines()
        f.close()
        f = open(logFile, 'w')
        for line in lines:
            line = re.sub(r'\[', '',line)
            line = re.sub(r'\]', '',line)
            line = re.sub(r'\'', '',line)
            line = re.sub(r'\\n', '',line)
            line = re.sub(r'\\t', '',line)
            line = re.sub(r',\s', ',',line)
            f.write(line)
        f.close()
    except IOError:
        sys.exit('IOError: No such file or directory. Check also the file permissions')


def ssh_conn(host,user,passwd,cmd):
    """Connect to each server in the serverlist file"""
    try:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host.strip(), username=user.strip(), password=passwd.strip(), timeout=60)
            stdin, stdout, stderr = ssh.exec_command(cmd.strip())
            logger_cmd(stdout,stderr)
        except paramiko.AuthenticationException:
            logger_gen(host.strip() + ',Authentication Error: Invalid username or password!')
        except paramiko.BadHostKeyException:
            logger_gen(host.strip() + ",SSH Error: server's host key could not be verified!")
        except paramiko.SSHException:
            logger_gen(host.strip() + ',SSH Error: there was an error connecting or establishing an SSH session')
        except socket.error:
            logger_gen(host.strip() + ',Socket Error: Connection Refused. Verify the server hostname or IP')
        except socket.gaierror:
            logger_gen(host.strip() + ',Socket Error: Name or service not known. Verify the server hostname or IP')
        except IOError:
            print 'IOError: Unable to log output file. Check directory permissions'
    finally:
        ssh.close()


def prog_check(processed_server,servercount):
    """Displays the progress in percentage in reference to the number of servers connected"""
    sys.stdout.write('\r')
    sys.stdout.write('%s %d%%' % ('Progress:',(100-(100*processed_server/servercount))))
    sys.stdout.flush()


def main():
    user, passwd, cmd = get_user_info()
    host, servers, servercount = get_serverlist()
    processed_server = servercount
    while (processed_server != 0):
        print 'Total number of servers:', servercount
        for host in servers:
            ssh_conn(host,user,passwd,cmd)
            prog_check(processed_server,servercount)
            processed_server = processed_server -1
        else:
            break
    logger_format()
    print ('............Done')


if __name__ == '__main__':
    main()
