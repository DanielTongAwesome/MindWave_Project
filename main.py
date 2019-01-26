from NeuroSky import NeuroPy
from queue import Queue
import threading
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


'''
record = NeuroPy(port="/dev/tty.MindWaveMobile-SerialPo-1")
record_thread = threading.Thread(target=record.start())
record_thread.start()
record_thread.join()
print("All Done")
'''

def NeuroSky_reader(q):
    record = NeuroPy(port="/dev/tty.MindWaveMobile-SerialPo-1", queue = q)
    record.start()


def data_reader(q):
    while(True):
        print(q.get())      
        

if __name__ == '__main__':
    q = Queue()
    t1 = threading.Thread(target=NeuroSky_reader, args=(q,))
    t2 = threading.Thread(target=data_reader, args=(q,))

    t1.start()
    t2.start()

    q.join()
    print('q joined!')


