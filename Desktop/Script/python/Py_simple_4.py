 #!/usr/bin/env python
# coding: UTF-8

import threading, Queue
import time, random, os

print time.ctime()

WORKERS = 3
mylock = threading.Lock()

def print1():
    os.system('sleep 5')
    print "123"

def print2():
    os.system('sleep 5')
    print "234"

def print3():
    os.system('sleep 5')
    print "345"

class Worker(threading.Thread):
    def __init__(self, queue):
        self.__queue = queue
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            item = self.__queue.get()
            mylock.acquire()
            #if item is None:
            #    break  # reached end of queue
                #pretend we're doing something that takes 1000 ms
            time.sleep(random.randint(10, 100) / 1000.0)
            print "task", item, "finished"
            mylock.release()

    # run with limited queue
queue = Queue.Queue(3)

for i in range(WORKERS):
    Worker(queue).start()  # start a worker

a = [print1(),print2(),print3()]

for item in a:
    print "push", item
    queue.put(item)

for j in range(WORKERS):
    queue.put(None)  # add end-of-queue markers


print time.ctime()
