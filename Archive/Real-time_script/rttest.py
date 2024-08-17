import multiprocessing
import time
import serial
import csv
import pandas as pd
import numpy as np


def datacol(conn):

    df = pd.read_csv('databig.csv')


    for i in range(1000):
        row=df.iloc[0]
        conn.send(row)
        print("Sent the message: {}".format(row))
        #time.sleep(0.5)

def receiver(conn):
    """
    function to print the messages received from other
    end of pipe
    """
    while 1:
        rec = conn.recv()
        if rec == "END":
            break
        #
        print("Received the message: {}".format(rec))
        #print(type(rec))
        time.sleep(10)


if __name__ == "__main__":
    # messages to be sent
    #msgs = ["hello", "hey", "hru?", "END"]

    # creating a pipe
    parent_conn, child_conn = multiprocessing.Pipe()

    # creating new processes
    p1 = multiprocessing.Process(target=datacol, args=(parent_conn,	))
    p2 = multiprocessing.Process(target=receiver, args=(child_conn,))

    # running processes
    p1.start()
    p2.start()

    # wait until processes finish
    p1.join()
    p2.join()