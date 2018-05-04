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
    port = 1112

    s = socket.socket()
    s.connect((host, port))
    # FileName = s.recv(1024)
    SumCurrent = ""
    counter = 1
    File_Name = ''
    FileData = ''
    while True:
        current = s.recv(1)
        current = str(current.decode())
        if current == '#' and counter == 1:
            File_Name = SumCurrent
            print("File Name to Node is " + File_Name)
            SumCurrent = ''
            counter += 1

        if current == '#' and counter == 2:
            FileData = SumCurrent
            FileData = FileData[1:]
            print("File data to Node is: " + FileData)

        SumCurrent += current
        if not current:
            break
    File = open(path + "/" + File_Name, "a+")
    File.write(FileData)
    # time.sleep(1)
    # FileName=str(FileName.decode())
    # FileData=s.recv(1024)
    # FileData=str(FileData.decode())

    # File = open(path+"/"+FileName, "a+")
    # File.write(FileData)


if __name__ == '__main__':
    Main()
