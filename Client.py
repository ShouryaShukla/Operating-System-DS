import os
import ntpath
import socket
import time
from os import listdir
from os.path import isfile, join
#import PyPDF2

path = 'ClientFolder'
if not os.path.exists(path):
    os.makedirs(path)

def sendFile(file):
    # File1 = open(file, "a+")
    # File1.close()
    File = open(file, "r")
    data = File.read()
    name = getFileName(file)
    return name, data


def getFileName(file):
    h, t = ntpath.split(file)
    return t or ntpath.basename(h)


def Main():
    # ip = socket.gethostname()
    ip = '127.0.1.1'
    host = ip
    port = 2221
    AllFiles = os.listdir(path)
    NumFiles = len(AllFiles)
    print("Number of files are: " + str(NumFiles))

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    print(onlyfiles)

    s = socket.socket()
    s.connect((host, port))
    # ss = s.recv(1024)
    # ss.decode()
    # filePath = raw_input(ss)
    # (file_name, file_data) = sendFile(filePath)

    # extt = file_name.split('.')
    # ext = extt[1]
    Send =''
    if NumFiles< 10:
        Send = '00'+str(NumFiles)
    elif 10< NumFiles and NumFiles < 100:
        Send = '0'+str(NumFiles)
    SendNum = str(Send).encode()
    s.send(SendNum)

    time.sleep(2)
    for file in onlyfiles:
        filePath = path+'/'+file
        print(filePath)
        (file_name, file_data) = sendFile(filePath)
        fn = (file_name + '#').encode() + (file_data + '$').encode()
        print("Extention "+fn)
        s.send(fn)
        time.sleep(5)
        # fd = file_data.encode()
        # s.send(fd)
        print("Name "+file_name)
        print("Data " + file_data)


    # Haven't been able to figure this part out
    # elif(ext=='pdf'):
    #     ...
    # elif (ext=='mp3'):
    #     ...
    # else:
    #     ...


if __name__ == '__main__':
    Main()











