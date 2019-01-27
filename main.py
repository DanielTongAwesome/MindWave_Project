from NeuroSky import NeuroPy
from queue import Queue
import threading
import logging
import time

# logging.basicConfig(level = logging.INFO, filename = "./records/" + time.strftime('%s.log'))

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

logging.basicConfig(level=logging.ERROR,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


def NeuroSky_reader(q):
    record = NeuroPy(port="/dev/rfcomm0", queue = q)
    logging.info("Start to recording the data .... ")
    record.start()


def data_reader(q):
    while(True):
        try:
            data = q.get()
            logging.info("Received Data: {}".format(data))
            print(data)
        except Exception as ex:
            logging.error("Error: {}".format(ex))

if __name__ == '__main__':
   
    q = Queue()
    t1 = threading.Thread(target=NeuroSky_reader, args=(q,))
    t2 = threading.Thread(target=data_reader, args=(q,))
    logging.info("MindWave Device Starts Working ....")
    t1.start()
    t2.start()

    q.join()
    #print('q joined!')

