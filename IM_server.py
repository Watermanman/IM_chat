import socket
import re
import queue
import threading

online={}
friendls={}
member={'Tom':"1234",'Marry':"1234",'Ken':"1234"}

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
        # data=conn.recv(1024).decode('ascii')
        # print(data)
        # if data:
        #     conn.sendall(b'login')
        #

class Newline(threading.Thread): 

    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock=sock
        
    def run(self):
        log_status=True
        while log_status:
            data=self.sock.recv(1024).decode('ascii')
            #print(data)   
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
                    else:
                        self.sock.sendall(b'pwER')
                else:
                    self.sock.sendall(b'unER')
        while True:
            data=self.sock.recv(1024).decode('ascii')
            cmd=re.match("(.*)\s(.*)\s(.*)",data)     #cmd(send,logout,friendlist...),...,... 
            #Normal cmd
            if cmd:
                if cmd.group(1)=="friendls":
                    if cmd.group(2)=="add": 
                        #add_friend 
                        friendls[self.usr].append(cmd.group(3))
                    elif cmd.group(2)=="rm":
                        #rm_friend
                        friendls[self.usr].remove(cmd.group(3))
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
                    if cmd.group(2) in online:
                        opt="{}:{}".format(self.usr,cmd.group(3))
                        online[cmd.group(2)].sendall(opt.encode('ascii'))
                    else:
                        print("{} is offline!".format(cmd.group(2)))
                        #print("say {} to {}".format(cmd.group(3),cmd.group(2)))
            else:
                print(str(self.ident)+"nonexsit cmd")

if __name__ =="__main__":
    server()
