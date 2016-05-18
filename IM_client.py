#!/usr/bin/env python3

import socket,threading,time
import getpass

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
            #print(self.usr+":"+say)
            # sdMsg="{} {}".format(self.usr,say)
            if(say=="logout" or say=="friendls"):
                say+="  "
            sock.sendall(say.encode('ascii'))
            if(say=="logout"):
                sock.close()
                 

class listen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            getMsg=sock.recv(1024)
        #getMsg="lister:hello~"
            if (getMsg):
                print("\n"+getMsg.decode('ascii'))
                # usr=getMsg[0:getMsg.index(":")]
                # content=getMsg[getMsg.index(":")+1:]
                # print("\n"+usr+":"+content)



if __name__ == "__main__":
    # sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # sock.connect(('127.0.0.1',2289))
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
