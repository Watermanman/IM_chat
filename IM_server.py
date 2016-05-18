import socket
import re
import queue
import threading

online={}

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
        data=self.sock.recv(1024).decode('ascii')
        #print(data)   
        log=re.match("@@@(.+),(.+)",data)
        if log:
            self.sock.sendall(b'login')
            online[log.group(1)]={self.sock}
            
            print("online:",end="")
            for i in online:
                print(i,end=" ")
            print(".")
        while True:
            data=self.sock.recv(1024).decode('ascii')
            cmd=re.match("(.*)\s(.*)\s(.*)",data)     #cmd(send,logout,friendlist...),...,... 
            if cmd:
                print(data)
                if cmd.group(1)=="logout":
                    print(self.ident)
                    self.sock.close()
                    break
                if cmd.group(1)=="send":
                    print("say {} to {}".format(cmd.group(3),cmd.group(2)))
            else:
                print(str(self.ident)+"nonexsit cmd")

if __name__ =="__main__":
    server()
