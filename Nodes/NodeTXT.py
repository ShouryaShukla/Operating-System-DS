import os
import socket
import time
#import PyPDF2

path = 'txtFolder'
if not os.path.exists(path):
    os.makedirs(path)

def Main():
    #ip = '127.0.1.1'
    host = socket.gethostbyname(socket.gethostname())
    port = 1111

    t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    t.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    t.bind((host, port))
    t.listen(1)
    d, addr = t.accept()
    print ("Connection from: " + str(addr))
    #s.connect((host, port))
    # FileName = s.recv(1024)
    # SumCurrent = ""
    # counter = 1
    # File_Name = ''
    # FileData = ''

    print("Text node connected to server " + str(addr[0]) + ":" + str(addr[1]))

    while True:
        size = d.recv(16)
        if not size:
            break
        size = int(size, 2)
        file_name = d.recv(size)

        file_size = d.recv(32)
        file_size = int(file_size, 2)
        block = 4096
        with open(os.path.join(path, file_name), 'wb') as f:
            while file_size > 0:
                if file_size < block:
                    block = file_size
                data = d.recv(block)
                f.write(data)
                file_size -= len(data)
        print("Received " + file_name)

    # while True:
    #     current = d.recv(1)
    #     current = str(current.decode())
    #     # print("Current: "+current)
    #     if current == '#' and counter == 1:
    #         file_name = SumCurrent
    #         #print("File Name is " + file_name)
    #         SumCurrent = ''
    #         counter += 1
    #         # print("Path is: " + path + "/" + file_name)
    #         File = open(path + "/" + file_name, "a+")
    #     if current == '$' and counter == 2:
    #         file_data = SumCurrent
    #         file_data = file_data[1:]
    #         print("File Name is " + file_name)
    #         print("File data is: " + file_data)
    #         extt = file_name.split('.')
    #         #ext = extt[1]
    #
    #         File.write(file_data)
    #         SumCurrent = ''
    #         current = ''
    #         counter = 1
            # print("Data is " + file_data)
    # while True:
    #     current = d.recv(1)
    #     current = str(current.decode())
    #     if current == '#' and counter == 1:
    #         File_Name = SumCurrent
    #         print("File Name to Node is " + File_Name)
    #         SumCurrent = ''
    #         counter += 1
    #
    #     if current == '$' and counter == 2:
    #         FileData = SumCurrent
    #         FileData = FileData[1:]
    #         print("File data to Node is: " + FileData)
    #
    #     SumCurrent += current
    #     SumCurrent += current
        # if not current:
        #     break

    # time.sleep(1)
    # FileName=str(FileName.decode())
    # FileData=s.recv(1024)
    # FileData=str(FileData.decode())

    # File = open(path+"/"+FileName, "a+")
    # File.write(FileData)
    #t.close()

if __name__ == '__main__':
    Main()
