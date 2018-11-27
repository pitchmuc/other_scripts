# -*- coding: utf-8 -*-
"""
from pitchmuc
"""
from ftplib import FTP
### example
host = 'myhost.com'
username = "username"
password="password"
_version='1.0.0'
def seeFile(host,user,mdp):
    with FTP(host) as ftp:
        ftp.login(user,mdp)
        print(ftp.nlst())
        return ftp.nlst()

def retrieveFileFTP(host,filename,user,mdp):
    fileName= filename
    localfile=open(filename, 'wb')
    with FTP(host) as ftp:   
        ftp.login(user,mdp)
        print(ftp.dir())
        ftp.retrbinary('RETR '+fileName,localfile.write,262144)
        localfile.close()

def deleteFileFTP(host,filename,user,mdp):
    fileName=filename
    with FTP(host) as ftp:
        ftp.login(user,mdp)
        ftp.delete(fileName)

def sendFile(host,filename,user,mdp):
    fileName=filename
    with FTP(host) as ftp:
        ftp.login(user,mdp)
        ftp.storlines('STOR '+fileName,open(fileName,'rb'))

seeFile(host,username,password)## print the file in the console
retrieveFileFTP('somefile.txt',host,username,password)
sendFile('somefile.txt',host,username,password)
deleteFileFTP('somefile.txt',host,username,password)