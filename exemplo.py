from multiprocessing.pool import ThreadPool
from threading import current_thread
from time import sleep

def say_hello():
    print(f"Hello! I'm thread {current_thread().getName()} saying hello!")
    sleep(1)

def main():
    threads = 4
    hellos = 20
    pool = ThreadPool(processes=threads)
    subprocess = []

    while(hellos >= 0):
        response = pool.apply_async( say_hello )
        subprocess.append(response)
        hellos -= 1
    pool.close()
    pool.join()
    for response in subprocess:
        try:
            response.get(timeout=30)
        except:
            print("Timeout error...")

if __name__ == "__main__":
    main()