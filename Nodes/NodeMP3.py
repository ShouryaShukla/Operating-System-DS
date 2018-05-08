import os
import socket
from os import listdir
from os.path import isfile, join
import time
#import PyPDF2

CliPath = os.getcwd()
path = CliPath
Pathtxt = os.getcwd() + '/MP3Folder'
if not os.path.exists(Pathtxt):
    os.makedirs(Pathtxt)


def sendFile(file):
    os.chdir(Pathtxt)
    File = open(file, "rb")
    data = File.read()
    return data

def Main():
    #ip = '127.0.1.1'
    host = socket.gethostbyname(socket.gethostname())
    port = 4444

    t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    t.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    t.bind((host, port))
    t.listen(1)
    d, addr = t.accept()
    print ("Connection from: " + str(addr))
    print("Text node connected to server " + str(addr[0]) + ":" + str(addr[1]))

    while True:
        name_size = d.recv(16)
        cnt_down = False
        if not name_size:
            break
        name_size = int(name_size, 2)
        #  print(name_size)
        time.sleep(2)
        file_name = d.recv(name_size).decode()
        print(file_name)

        if file_name[-1] == '#':
            file_name = file_name[:-1]
            # print(file_name)
            cnt_down = True


        if cnt_down is False:
            file_size = d.recv(32)
            file_size = int(file_size, 2)
            chunk = 4096
            os.chdir(Pathtxt)
            with open(os.path.join(Pathtxt, file_name), 'wb') as f:
                while file_size > 0:
                    if file_size < chunk:
                        chunk = file_size
                    data = d.recv(chunk)
                    f.write(data)
                    file_size -= len(data)
            print("Received " + file_name)


        elif cnt_down is True:

            #  print("Counter Ack")
            folder = "/MP3Folder"
            Path = CliPath + folder
           #   print("Path is:"+Path)
            if not os.path.exists(Path):
                os.makedirs(Path)
            onlyfiles = [fl for fl in listdir(Pathtxt) if isfile(join(Pathtxt, fl))]

            if file_name in onlyfiles:
                print("Sending " + file_name)
                size = len(file_name)
                size = bin(size)[2:].zfill(16)
                #  print(size)
                d.send(size)
                time.sleep(2)
                d.send(file_name)

                file_path = os.path.join(Path, file_name)
                file_size = os.path.getsize(file_path)
                file_size = bin(file_size)[2:].zfill(32)
                d.send(file_size)
                data = sendFile(file_name)
                d.sendall(data)
                print("Sent: " + file_name)
            else:
                print("No such File")

if __name__ == '__main__':
    Main()
