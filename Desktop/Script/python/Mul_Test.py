#!/usr/bin/python
# -*- coding: UTF-8 -*-

import multiprocessing
import wx

def consumer(input_q):
    while True:
        item = input_q.get()
        if item is None:
            break
        print(item)
    print("Consumer done")
        #input_q.task_done()

def producer(sequence,output_q):
    for item in sequence:
        output_q.put(item)

if __name__ == '__main__':
    q = multiprocessing.JoinableQueue()
    cons_p = multiprocessing.Process(target=consumer,args=(q,))
    cons_p.daemon = True
    cons_p.start()

    sequence = [1,2,3,4]
    producer(sequence,q)

    q.put(None)

    cons_p.join()
