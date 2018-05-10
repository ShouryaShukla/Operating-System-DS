import sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import ntpath
import socket
import time
from os import listdir
from os.path import isfile, join
import threading
from threading import Lock
#import PyPDF2

path = 'ClientFolder'
if not os.path.exists(path):
    os.makedirs(path)

ip = socket.gethostname()
#ip = '127.0.1.1'
#ip='10.1.22.17'
host = ip
port = 2221

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print ('Connection established')

lock = Lock()


class MyHandler(PatternMatchingEventHandler):


    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug
        return event.src_path, event.event_type

    def on_modified(self, event):

        lock.acquire()
        (x,y) = self.process(event)

        if('/' in x):
            file=x[x.rfind('/')+1:]
        else:
            file=x[x.rfind("\\")+1:]
        print("Syncing " + file)
        size = len(file)
        size = bin(size)[2:].zfill(16)
        #print(size)
        s.send(size)
        time.sleep(2)
        s.send(file)

        file_size = os.path.getsize(x)
        file_size = bin(file_size)[2:].zfill(32)
        s.send(file_size)
        data = sendFile(x)
        s.sendall(data)
        print("Sent: "+file)

        lock.release()


    def on_created(self, event):
        lock.acquire()
        (x,y)=self.process(event)

        if('/' in x):
            file=x[x.rfind('/')+1:]
        else:
            file=x[x.rfind("\\")+1:]
        print("Syncing " + file)
        size = len(file)
        size = bin(size)[2:].zfill(16)
        #print(size)
        s.send(size)
        time.sleep(2)
        s.send(file)

        file_size = os.path.getsize(x)
        file_size = bin(file_size)[2:].zfill(32)
        s.send(file_size)
        data = sendFile(x)
        s.sendall(data)
        print("Sent: "+file)

        lock.release()


    def on_query(self):
        lock.acquire()
        down = raw_input("Enter file to be Downloaded: ")

        print("Downloading: " + down)

        down += "#"

        size1 = len(down)

        size1 = bin(size1)[2:].zfill(16)

        s.send(size1)

        time.sleep(2)

        s.send(down)

        size = s.recv(16)

        if not size:
            lock.release()
            return

        size = int(size, 2)

        file_name = s.recv(size)

        file_size = s.recv(32)

        file_size = int(file_size, 2)

        chunk = 4096

        folder = "DownFiles"

            # Path = CliPath + folder
            #
            # if not os.path.exists(Path):
            #
            #     os.makedirs(Path)
            #
            # #os.chdir(Path)

        with open(os.path.join(folder, file_name), 'wb') as f:

            while file_size > 0:

                if file_size < chunk:

                    chunk = file_size

                data = s.recv(chunk)

                f.write(data)

                file_size -= len(data)

        print("Received " + file_name)
        lock.release()



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
    path='ClientFolder'
    onlyfiles = [fl for fl in listdir(path) if isfile(join(path, fl))]
    print(onlyfiles)
    observer = Observer()
    observer.schedule(MyHandler(), path='ClientFolder')
    observer.start()

    try:
        while True:
            ask = raw_input("Download file? y/n: ")

            if str(ask) == 'y':
                O1=MyHandler()
                O1.on_query()
                time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()



if __name__ == '__main__':
    Main()