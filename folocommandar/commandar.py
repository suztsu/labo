import socket
import string

host = 'localhost'
port = 10500

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

recvdata = ""

while True:
    while (recvdata.find("\n.") == -1):
        recvdata = recvdata + sock.recv(1024)
    
    temp = ""
    for line in recvdata.split('\n'):
        i = line.find('WORD="')
        if i != -1:
            line = line[i + 6:line.find('"', i + 6)]
            temp = temp + line
    
    print("結果:" + temp)
    recvdata = ""
