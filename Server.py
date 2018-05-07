import socket
import os
import time
#import PyPDF2

ServerFile = open('Server File.txt', "a+")

def Main():
    host = socket.gethostbyname(socket.gethostname())
    port = 2221
    txtPort= 1111
    pdfPort= 3333
    mp3Port= 4444
    otherPort= 5555
    index = {}
    storage = {"txt": txtPort, "pdf": pdfPort, "mp3": mp3Port, "other": otherPort}
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))

    s.listen(1)
    print("Server is now listening at-"+host)
    c, addr = s.accept()
    print ("Connection from: " + str(addr))

    t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    t.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    t.connect((host, txtPort))

    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    p.connect((host, pdfPort))

    m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    m.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    m.connect((host, mp3Port))

    o = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    o.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    o.connect((host, otherPort))

    while True:
        size = c.recv(16)
        cnt_down = False
        # print(size)
        if not size:
            break
        name_size = int(size, 2)
        file_name = c.recv(name_size).decode()
        if file_name[-1] == '#':
            file_name = file_name[:-1]
            size = len(file_name)
            cnt_down = True
        print(file_name)

        file_type = file_name[file_name.index('.') + 1:]
        if file_type != "txt" and file_type != "pdf" and file_type != "mp3":
            file_type = "other"


        if file_type == "txt":
            typ = t
        elif file_type == "pdf":
            typ = p
        elif file_type == "mp3":
            typ = m
        else:
            typ = o


        if cnt_down == False:
            size = len(file_name.encode())
            size = bin(size)[2:].zfill(16)
            typ.send(size)

            index[file_name] = storage[file_type]

            typ.send(file_name.encode())

            file_size = c.recv(32)
            typ.send(file_size)
            time.sleep(2)
            file_size = int(file_size, 2)
            block = 4096
            while file_size > 0:
                if file_size < block:
                    block = file_size
                data = c.recv(block)
                typ.send(data)
                file_size -= len(data)
            ServerFile.write(str(index))

        if cnt_down == True:  # When server has to download to client
            file_name += '#'

            print("Sending "+file_name)


            size1 = len(file_name.encode())
            size1 = bin(size1)[2:].zfill(16)
            typ.send(size1)
            time.sleep(2)
            typ.sendall(file_name.encode())  # Sent file_name size and file_name to Node


            sizefn = typ.recv(16)  # Getting file_name size from Node
            print(sizefn)
            if not sizefn:
                break
            sizefn = int(sizefn, 2)
            file_name = typ.recv(sizefn)  # Getting file_name from Node
            print("Server Got Name "+file_name)
            file_size = typ.recv(32)
            file_size = int(file_size, 2)  # File_data size
            print("Size is "+str(file_size))
            chunk = 4096
            full_data = ""
            while file_size > 0:  # File_data
                if file_size < chunk:
                    chunk = file_size
                data = typ.recv(chunk)
                full_data += data
                file_size -= len(data)

            print("Received From Node: " + file_name)
            size = len(file_name)
            size = bin(size)[2:].zfill(16)
            c.send(size)
            c.send(file_name)
            file_size = len(full_data)
            file_size = bin(file_size)[2:].zfill(32)
            c.send(file_size)
            print("Full data is "+full_data)
            c.sendall(full_data)  # Sending file data

    c.close()


if __name__ == '__main__':
    Main()
