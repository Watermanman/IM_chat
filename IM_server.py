import socket
import re
import queue
import threading
from datetime import datetime

online={}
friendls={}
member={'Tom':"1234",'Marry':"1234",'Ken':"1234"}
offlineMsg={}

def server():
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr=("127.0.0.1",2290)
    server.bind(server_addr)
    server.listen(100)
    print("server on",server.getsockname())
    conn=queue.Queue(maxsize=100)    
    while True:
        sock,addr=server.accept()
        conn.put(Newline(sock).start()) 

class Newline(threading.Thread): 

    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock=sock
        
    def run(self):
        log_status=True
        while log_status:
            data=self.sock.recv(1024).decode('ascii')
            log=re.match("@@@(.+),(.+)",data)
            if log:
                if log.group(1) in member:
                    if log.group(2) == member[log.group(1)]:
                        self.sock.sendall(b'logok')
                        self.usr=log.group(1)
                        friendls[self.usr]=[]
                        online[log.group(1)]=self.sock
                        print("online:",end="")
                        for i in online:
                            print(i,end=" ")
                        print(".")
                        log_status=False
                        #======================offlineMsg============================
                        if self.usr in offlineMsg: 
                            if len(offlineMsg[self.usr])>0:
                                offmsg=""
                                offmsg+="========You have offlineMsg========\n"
                                for i in offlineMsg[self.usr]:
                                    offmsg+=i
                                    offmsg+="\n"
                                self.sock.sendall(offmsg.encode('ascii'))
                        #==========================================================
                    else:
                        self.sock.sendall(b'pwER')
                else:
                    self.sock.sendall(b'unER')
                        
        while True:
            data=self.sock.recv(1024).decode('ascii')
            cmd=re.match("(.*)\s(.*)\s(.*)",data)     #cmd(send,logout,friendlist...),...,... 
            #Normal cmd
            if cmd:
                if cmd.group(1)=="sendfile":
                    if cmd.group(2) in online:
                        opt="Do you want to get file from {}?(Y/N)".format(self.usr)
                        online[cmd.group(2)].sendall(opt.encode('ascii'))
                        ans=""
                        while ans=="":
                            print("watit recv")
                            ans=online[cmd.group(2)].recv(1024).decode('ascii')
                        if ans =="y" or ans=="Y":
                            while True:
                                print("wait data")    
                            # self.sock.sendall(b'pushdata')
                            # datafile=self.sock.recv(1024)
                            print("start")
                        elif ans=="n" or ans=="N":
                            opt="{} disagree!!".format(cmd.group(2))
                            self.sock.sendall(opt.encode('ascii'))
                if cmd.group(1)=="friendls":
                    if cmd.group(2)=="add": 
                        #add_friend 
                        if cmd.group(3) in member:
                            friendls[self.usr].append(cmd.group(3))
                            self.sock.sendall(b'add done')
                        else:
                            self.sock.sendall(b'non exists member')
                    elif cmd.group(2)=="rm":
                        #rm_friend
                        if cmd.group(3) in friendls[self.usr]:
                            friendls[self.usr].remove(cmd.group(3))
                            self.sock.sendall(b'rm done')
                        else:
                            self.sock.sendall(b'non exists friend')
                    else:
                        fls=""
                        fls+="Your firend list\n"
                        for i in friendls[self.usr]:
                            fls+=i
                            if i in online:
                                fls+="\tonline\n"
                            else:
                                fls+="\tofflie\n"
                        self.sock.sendall(fls.encode('ascii'))
                        
                if cmd.group(1)=="logout":
                    print(self.usr+" logout")
                    online.pop(self.usr)
                    print("online:",end="")
                    for i in online:
                        print(i,end=" ")
                    print(".")
                    self.sock.close()
                    break
                if cmd.group(1)=="send":
                    opt="{}:{}".format(self.usr,cmd.group(3))
                    if cmd.group(2) in member:
                        if cmd.group(2) in online:
                            #opt="{}:{}".format(self.usr,cmd.group(3))
                            online[cmd.group(2)].sendall(opt.encode('ascii'))
                        else:
                            opt+="\t"
                            time=datetime.strftime(datetime.now(),"%y-%m-%d %H:%M:%S")
                            opt+=time
                            offlineMsg[cmd.group(2)]=[]
                            offlineMsg[cmd.group(2)].append(opt)
                            msg="{} is offine!".format(cmd.group(2)) 
                            self.sock.sendall(msg.encode('ascii'))
                    else:
                        self.sock.sendall(b'Non exist Member')
            else:
                print("nonexsit cmd")

if __name__ =="__main__":
    server()
