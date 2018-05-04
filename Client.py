import os
import ntpath
import socket
import PyPDF2

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
    ip='10.1.33.18'
    host = ip
    port = 2222

    s = socket.socket()
    s.connect((host, port))
    ss=s.recv(1024)
    ss.decode()
    filePath=raw_input(ss)
    (file_name, file_data)=sendFile(filePath)

    extt=file_name.split('.')
    ext=extt[1]


    if(ext=='txt'):
        fn=file_name.encode()
        s.send (fn)

        fd=file_data.encode()
        s.send(fd)


    # Haven't been able to figure this part out
    # elif(ext=='pdf'):
    #     ...
    # elif (ext=='mp3'):
    #     ...
    # else:
    #     ...



if __name__ == '__main__':
    Main()











