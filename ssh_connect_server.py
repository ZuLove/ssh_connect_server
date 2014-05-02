#!/usr/bin/python
#-*- coding:utf-8 -*-

import paramiko,time
import os,datetime


server_ip = '192.168.40.200'
server_user = 'root'
server_passwd = 'myxiayi123'
server_port = 22
local_dir = r'D:\wins\data'
#local_dir = r'D:\wins\log_backup'

remote_dir ='/home/mysql_data/'
#remote_dir = '/home/test/'

#从windows上将文件上传至linux
def ssh_win_to_linux(local_dir,remote_dir):
    print os.path.exists(local_dir),os.path.isdir(local_dir)
    client = paramiko.Transport((server_ip,server_port))
    client.connect(username=server_user, password=server_passwd)
    sftp = paramiko.SFTPClient.from_transport(client)
    startime = time.time()
    length = len(local_dir)+1
    for root,dirs,files in os.walk(local_dir):

        for filex in files:
            dir_path = ''
            strx = os.path.split(os.path.join(root,filex)[length:])[0]
            if strx:
                dir_path = strx.replace('\\','/')
                cmdStr = 'mkdir '+remote_dir+dir_path
                ssh_exec_command(cmdStr)
            print 'Uploading file:',os.path.join(root,filex)
            sftp.put(os.path.join(root,filex),os.path.join(remote_dir+dir_path+'/',filex))
            print 'Uploading file success....'
    print 'Total time:',time.time()-startime
    client.close()

#远程执行命令
def ssh_exec_command(cmdStr):
        paramiko.util.log_to_file('paramiko.log')    
        ssh=paramiko.SSHClient()   
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
        ssh.connect(hostname = server_ip,username=server_user, password=server_passwd)    
        stdin,stdout,stderr=ssh.exec_command(cmdStr)    
        print stdout.read()    
        ssh.close()
#远程下载文件
def ssh_linux_to_win(local_dir,remote_dir):
    client = paramiko.Transport((server_ip,server_port))
    client.connect(username=server_user, password=server_passwd)
    sftp = paramiko.SFTPClient.from_transport(client)
    #files = sftp.listdir_attr(remote_dir)
    files = sftp.listdir(remote_dir)
    startime = time.time()
    for filex in files:
        print 'DownLoading file:',os.path.join(remote_dir,filex)
        sftp.get(os.path.join(remote_dir,filex),os.path.join(local_dir,filex))
        print 'Download file success %s ' % datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    endtime = time.time()
    print 'Total time:',endtime-startime
    client.close()
    
if __name__ == '__main__':
        #ssh_exec_command()
        ssh_linux_to_win(local_dir,remote_dir)
        #ssh_win_to_linux(local_dir,remote_dir)
