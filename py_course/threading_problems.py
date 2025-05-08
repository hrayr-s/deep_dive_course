import threading
from queue import Queue
from time import sleep
from typing import Dict

global_queue = Queue()


def handler():
    for i in range(100):
        sleep(1)
        f = open('log.txt', 'a+')
        f.write(f"hello - Done {i} for {threading.current_thread().ident}\n")
        f.close()


def sleep_threads(sleep_for: int) -> None:
    # if sleep_for % 3 == 0:
    #     perp = 0
    #     while perp < 1_000_000_000:
    #         perp += 1

    sleep(sleep_for)
    print(f'Thread #{threading.current_thread().name} slept for ' + str(sleep_for) + ' seconds...')


def main():
    thread_pool = []
    for i in range(100):
        t = threading.Thread(target=sleep_threads, daemon=True, args=(5,))
        thread_pool.append(t)
        t.start()

    print('\n')
    while all([thread_pool[i].is_alive() for i in range(100)]):
        print(f'Threads active: {threading.active_count()}', end='\r')
        # print(f'Threads active: {threading.')


if __name__ == '__main__':
    main()
