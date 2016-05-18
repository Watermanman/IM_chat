#!/usr/bin/env python3

import socket,threading,time


def chklog():
    user=input("username:")
    pw=input("password:")
    #data="{},{}".format(user,pw)
    return user,pw

class enter(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.usr=name

    def run(self):
        while True:
            say=input(">>>")
            print(self.usr+":"+say)
            # sdMsg="{} {}".format(self.usr,say)
            sock.sendall(say.encode('ascii'))
            if(say=="logout"):
                sock.close()


class listen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # getMsg=sock.recv(1024)
        getMsg="lister:hello~"
        # if (getMsg):
        #     usr=getMsg[0:getMsg.index(":")]
        #     content=getMsg[getMsg.index(":")+1:]
        #     print("\n"+usr+":"+content)



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
        if msg=="login":
            print("logOK")
            login=False
        else:
            print("log error")
            sock.close()

    th_enter=enter(usr)
    th_listen=listen()
    th_enter.start()
    th_listen.start()
