import os
import ntpath
import socket

path = 'C:\Users\shourya\PycharmProjects\OSAssignment3\ClientFolder'
if not os.path.exists(path):
    os.makedirs(path)

File1= open("C:\Users\shourya\PycharmProjects\OSAssignment3\ClientFolder\File1.txt", "r")
def sendFile(file):
    File= open(file, "r")
    data=File.read()
    name=findFileName(file)
    return (name, data)


def findFileName(file):
    h,t = ntpath.split(file)
    return t or ntpath.basename(h)


def Main():
    ip = socket.gethostname()
    host = ip
    port = 2345

    s = socket.socket()
    s.connect((host, port))
    print(s.recv(1024))
    filePath=raw_input("Enter file path: ")
    (file_name, file_data)=sendFile(filePath)
    s.send(file_name)
    s.send(file_data)


if __name__ == '__main__':
    Main()



newpath = 'C:\Users\shourya\PycharmProjects\OSAssignment3\ClientFolder'
if not os.path.exists(newpath):
    os.makedirs(newpath)







