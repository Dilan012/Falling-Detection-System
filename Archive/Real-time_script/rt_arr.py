import multiprocessing
import time
import serial
import csv
import numpy as np


def datacol(conn):

    ser = serial.Serial('COM9', 9600)  # Replace with the correct port name

    start_time=time.time()

    for i in range(10):
        try:
            line = ser.readline().decode().strip()
            values = line.split(',')
        except:
            # ignore the error and continue
            continue
        #print(line)
        #values = line.split(',')
        if len(values) != 6:
            continue
        try:
            accel_x = float(values[0])
            accel_y = float(values[1])
            accel_z = float(values[2])
            gyro_x = float(values[3])
            gyro_y = float(values[4])
            gyro_z = float(values[5])
        except ValueError:
            continue

        row=[accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z]

        conn.send(row)
        #print("Sent the message: {}".format(row))
        print("SENT",i)
        #time.sleep(0.5)

    end_time = time.time()
    dt=end_time - start_time
    print("DT:", dt)
    conn.send("END")
        
    conn.close()

    ser.close()

def receiver(conn):
    #time.sleep(8)
    j=0
    arr = np.array([['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z']])
    while 1:
        rec = conn.recv()
        if rec == "END":
            break
        j=j+1
        #print("Received the message: {}".format(rec))
        print("REC",j)
        #print(type(rec))
        arr=np.vstack([arr, np.array(rec)])










        

if __name__ == "__main__":

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
