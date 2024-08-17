import multiprocessing
import time
import serial
import csv


def datacol(conn):

    ser = serial.Serial('COM9', 9600)  # Replace with the correct port name

    start_time=time.time()

    for i in range(10):
        line = ser.readline().decode().strip()
        #print(line)
        values = line.split(',')
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
        print("Sent the message: {}".format(row))
        #time.sleep(0.5)

    end_time = time.time()
    dt=end_time - start_time
    print("DT:", dt)
        
    conn.close()

    ser.close()

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
        print(type(rec))


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