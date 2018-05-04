import os
import socket
import time
#import PyPDF2

path = 'txtFolder'
if not os.path.exists(path):
    os.makedirs(path)

def Main():
    ip = '127.0.1.1'
    host = ip
    port = 1111

    s = socket.socket()
    s.connect((host, port))
    FileName=s.recv(1024)
    time.sleep(1)
    FileName=str(FileName.decode())
    FileData=s.recv(1024)
    FileData=str(FileData.decode())

    File= open(path+"/"+FileName, "a+")
    File.write(FileData)


if __name__ == '__main__':
    Main()
