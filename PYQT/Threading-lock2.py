import threading

tot = 0
lock = threading.Lock()

def add_total(amount):
    global tot
    lock.acquire()
    try:
        tot += amount
    finally:
        lock.release()
    print(threading.currentThread().getName()+' Synchronized: '+tot)

if __name__ == '__main__':
    for i in range(10000):
        my_thread = threading.Thread(
            target = add_total, args=(1,))
    my_thread.start()