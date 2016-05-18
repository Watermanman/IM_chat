#!/usr/bin/env python3

import socket,threading,time
import getpass
import os
import re

def chklog():
    user=input("Username: ")
    pw=getpass.getpass()
    #data="{},{}".format(user,pw)
    return user,pw

class enter(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.usr=name

    def run(self):
        while True:
            say=input(">>>")
            sendfile=re.match("sendfile (.+) (.+)",say)
            if sendfile:
                filename=sendfile.group(2)
                if os.path.exists(filename):
                    sock.sendall(say.encode('ascii'))
                else:
                    print("The file non exists")
            else:
                if(say=="n" or say=="N" or say=="y" or say=="Y"):
                    sock.sendall(b'  ')
                if(say=="logout" or say=="friendls"):
                    say+="  "
                sock.sendall(say.encode('ascii'))
                if(say=="logout"):
                    sock.close()
                    break
                 

class listen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            getMsg=sock.recv(1024)
            if (getMsg):
                print("\n"+getMsg.decode('ascii'))



if __name__ == "__main__":
    login=True
    while login:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect(('127.0.0.1',2290))
        usr,pw=chklog()
        loginfo="@@@{},{}".format(usr,pw)
        sock.sendall(loginfo.encode('ascii'))
        msg=sock.recv(1024).decode('ascii')
        if msg=="logok":
            print("Sign-in sucessful")
            login=False
        elif msg=="pwER":
            print("Password error")
            sock.close()
        elif msg=="unER":
            print("Username error")
            sock.close()
        else:
            print("Log error")
            sock.close()

    th_enter=enter(usr)
    th_listen=listen()
    th_enter.start()
    th_listen.start()
