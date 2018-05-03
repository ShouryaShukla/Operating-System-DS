import os
import ntpath
import socket

path = 'ClientFolder'
if not os.path.exists(path):
    os.makedirs(path)


def sendFile(file):
    File1=open(file, "a+")
    File1.close()
    File= open(file, "r")
    data=File.read()
    name=findFileName(file)
    return (name, data)


def findFileName(file):
    h,t = ntpath.split(file)
    return t or ntpath.basename(h)


def Main():
    # ip = socket.gethostname()
    ip='10.1.31.37'
    host = ip
    port = 1115

    s = socket.socket()
    s.connect((host, port))
    ss=s.recv(1024)
    ss.decode()
    print(ss)
    filePath=raw_input("Enter file path: ")
    (file_name, file_data)=sendFile(filePath)
    fn=file_name.encode()
    s.send (fn)
    fd=file_data.encode()
    s.send(fd)



if __name__ == '__main__':
    Main()











