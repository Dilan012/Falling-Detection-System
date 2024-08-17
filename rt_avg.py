import multiprocessing
import time
import serial
import csv
import numpy as np
import pandas as pd
import joblib



def datacol(conn):

    ser = serial.Serial('COM9', 9600)  # Replace with the correct port name

    start_time=time.time()

    for i in range(155):
        try:
            line = ser.readline().decode().strip()
            #print(line)
            values = line.split(',')
        except:
            # Ignore errors and continue
            #print('err')
            continue

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
        #print("SENT",i)
        #time.sleep(0.5)

    end_time = time.time()
    dt=end_time - start_time
    print("DT:", dt)
    conn.send("END")
        
    conn.close()

    ser.close()
    print("p1 finished")

def receiver(conn):
    #time.sleep(8)
    j=0
    #arr = np.array([['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z']])
    arr = np.empty((0, 6))
    knn_model = joblib.load('model_avg.pkl')
    banner="  ______ ___   _      _          ______ _____ _____ _____ _____ _____ ___________ \n  |  ___/ _ \ | |    | |         |  _  \  ___|_   _|  ___/  __ \_   _|  ___|  _  \ \n  | |_ / /_\ \| |    | |         | | | | |__   | | | |__ | /  \/ | | | |__ | | | | \n  |  _||  _  || |    | |         | | | |  __|  | | |  __|| |     | | |  __|| | | | \n  | |  | | | || |____| |____     | |/ /| |___  | | | |___| \__/\ | | | |___| |/ / \n  \_|  \_| |_/\_____/\_____/     |___/ \____/  \_/ \____/ \____/ \_/ \____/|___/  "
    for i in range(8):
        rec = conn.recv()
        print("REC",j)
        j=j+1
        arr = np.vstack([arr, np.array(rec)])
    while 1:

        print(arr) # 
        if j!=8:
            arr = arr[7:, :]
        for i in range(7):
            
            rec = conn.recv()
            print("REC",j)
            j=j+1
            if rec == "END":
                break

            #print("Received the message: {}".format(rec))
            
            arr = np.vstack([arr, np.array(rec)])

            if arr.shape[0]==15:
                df=pd.DataFrame(arr)
                #print(df)

                # Calculate magnitude of accl readings
                df['Acc_Magnitude'] = df.apply(lambda x: np.sqrt(x[0]**2 + x[1]**2 + x[2]**2), axis=1)

                # Calculate magnitude of gyro readings
                df['Gyro_Magnitude'] = df.apply(lambda x: np.sqrt(x[3]**2 + x[4]**2 + x[5]**2), axis=1)

                avg=df.iloc[:, -2:].mean()
                avgdf=pd.DataFrame([avg])
                print(avgdf)

                # Make predictions on the new data using the loaded KNN model
                predictions = knn_model.predict(avgdf)
                print("pred",predictions)
                if predictions[0]==1 or predictions[0]=='1':
                    print(banner)
                    #input("press key to cont.")
                    #print("Continuing...")
                    time.sleep(120)



            
        #print(arr)
        #df = pd.DataFrame(arr)
        #print(df)
        if rec == "END":
            break
            
    print("p2 finished")
##    df = pd.DataFrame(arr)
##    print(df)










        

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
