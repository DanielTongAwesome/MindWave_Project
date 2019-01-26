from NeuroSky import NeuroPy
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )



def stop_thread(thread):
    thread.stop()
    thread.save()


person_name = input('Name: ')
task_name = input('Task Name: ')
task_duration = input('Duration of the Test(in sec): ')

record = NeuroPy("COM3", person_name=person_name, task_name=task_name, task_duration=task_duration)
threading.Timer(int(task_duration), stop_thread, [record]).start()
record.start()
