import os
import ntpath
import socket
import time
from os import listdir
from os.path import isfile, join
#import PyPDF2


CliPath = os.getcwd()
path = CliPath +'/ClientFolder'
if not os.path.exists(path):
    os.makedirs(path)

def sendFile(file):
    # File1 = open(file, "a+")
    # File1.close()
    File = open(file, "rb")
    data = File.read()
    # name = getFileName(file)
    return data


def Main():
    # ip = socket.gethostname()
    ip = '127.0.1.1'
    host = ip
    port = 2221

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    ask = ''
    while ask != '4':
        #  print("path is "+path)
        onlyfiles = [fl for fl in listdir(path) if isfile(join(path, fl))]
        #  print(onlyfiles)
        os.chdir(path)

        ask = raw_input("Input 1 for sync, 2 for Download, 3 for check file, 4 for quit")
        if ask == '4':
            s.close()
            break

        if str(ask) == '1':
            for file in onlyfiles:
                print("Sending " + file)
                size = len(file)
                size = bin(size)[2:].zfill(16)
                #  print(size)
                s.send(size)
                time.sleep(2)
                s.send(file)

                file_path = os.path.join(path, file)
                file_size = os.path.getsize(file_path)
                file_size = bin(file_size)[2:].zfill(32)
                s.send(file_size)
                data = sendFile(file)
                s.sendall(data)
                print("Sent: "+file)

        elif str(ask) == '2':
            down = raw_input("Enter file to be Downloaded")
            print("Downloading: " + down)
            down += "#"
            size1 = len(down)
            size1 = bin(size1)[2:].zfill(16)
            s.send(size1)
            time.sleep(2)
            s.send(down)

            size = s.recv(16)
            if not size:
                break
            size = int(size, 2)
            file_name = s.recv(size)
            file_size = s.recv(32)
            file_size = int(file_size, 2)
            chunk = 4096
            folder = "/DownFiles"
            Path = CliPath + folder
            if not os.path.exists(Path):
                os.makedirs(Path)
            #os.chdir(Path)
            with open(os.path.join(Path, file_name), 'wb') as f:
                while file_size > 0:
                    if file_size < chunk:
                        chunk = file_size
                    data = s.recv(chunk)
                    f.write(data)
                    file_size -= len(data)
            print("Received " + file_name)

        elif str(ask) == '3':
            print("Fetching List of Files")
            Check = '$'
            sizeCh = len(Check)
            sizeCh = bin(sizeCh)[2:].zfill(16)
            s.send(sizeCh)
            time.sleep(2)
            s.send(Check)

            sizerc = s.recv(16)
            if not sizerc:
                break
            sizerc = int(sizerc, 2)
            listeles = s.recv(sizerc).decode()
            print("The files and their corresponding nodes are: " + str(listeles))






if __name__ == '__main__':
    Main()











