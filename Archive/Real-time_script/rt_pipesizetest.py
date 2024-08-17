import multiprocessing
import time
import serial
import csv
import pandas as pd
import numpy as np


def datacol(conn):

    df = pd.read_csv('bigdata.csv')


    for i in range(100):
        row=df.iloc[i]
        conn.send(row)
        print("Sent",i)
        #print("Sent the message: {}".format(row))
        #time.sleep(0.5)
    conn.close()
    
def receiver(conn):
    """
    function to print the messages received from other
    end of pipe
    """
    time.sleep(3)
    with open('databig.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        j=0
        while 1:
            rec = conn.recv()
            if j == 100:
                break
            csvwriter.writerow(rec)
            print("Received",j)
            j=j+1
            #print("Received the message: {}".format(rec))
            #print(type(rec))
            #time.sleep(10)
    conn.close()
    


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