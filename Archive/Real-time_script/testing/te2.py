import multiprocessing
import time

def count(from_num, to_num):
    for i in range(from_num, to_num+1):
        print(i)
        time.sleep(0.3)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=count, args=(1, 3))
    p2 = multiprocessing.Process(target=count, args=(4, 6))
    p3 = multiprocessing.Process(target=count, args=(7, 10))
    
    p1.start()
    p2.start()
    p3.start()
    
    p1.join()
    p2.join()
    p3.join()
