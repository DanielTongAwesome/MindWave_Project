from NeuroSky import NeuroPy
from queue import Queue
import threading
import logging
import sys
import serial
import time
import datetime
import math
from os import path

print(sys.version)

#import for PyQt
from PyQt4.QtGui import QApplication, QMainWindow, QWidget, QPen, QColor, QGraphicsItem
from PyQt4.QtCore import Qt, QThread, pyqtSignal, QDate, QTimer

#import for Matplotlib
import numpy as np
import pyqtgraph as pg
import random

from mind_tello import Ui_MainWindow
from main_qt import main

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

# global queue
q = Queue()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, headless=False):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.headless = headless
        self.setWindowModality(Qt.ApplicationModal)
        self.update_date()
        self.setup_graph()
        self.run_thread()

    def update_date(self):
        self.start_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.curr_day = QDate.currentDate().toString('MMMM d, yyyy')
        self.date.setText(self.curr_day)

    def setup_graph(self):
        # set up plots of data flow
        # generic chunk settings
        self.chunk_size = 100
        self.max_chunks = 10
        self.start_time = pg.ptime.time()
        # delta
        self.delta_wave_plot = pg.PlotWidget()
        self.delta_wave_plot.setXRange(-10,0)
        self.data_to_plot_delta = np.empty((self.chunk_size+1,2))
        self.ptr_0 = 0
        self.curves_0 = []
        self.delta_wave_plot.plotItem.plot()
        self.delta_wave.addWidget(self.delta_wave_plot)       
        # theta
        self.theta_wave_plot = pg.PlotWidget()
        self.theta_wave_plot.setXRange(-10,0)
        self.data_to_plot_theta = np.empty((self.chunk_size+1,2))
        self.ptr_1 = 0
        self.curves_1 = []
        self.theta_wave_plot.plotItem.plot()
        self.theta_wave.addWidget(self.theta_wave_plot)       
        # alpha_low
        self.alpha_low_wave_plot = pg.PlotWidget(title="Low")
        self.alpha_low_wave_plot.setXRange(-10,0)
        self.data_to_plot_alpha_low = np.empty((self.chunk_size+1,2))
        self.ptr_2 = 0
        self.curves_2 = []
        self.alpha_low_wave_plot.plotItem.plot
        self.alpha_low_wave.addWidget(self.alpha_low_wave_plot)     
        # alpha_high
        self.alpha_high_wave_plot = pg.PlotWidget(title="High")
        self.alpha_high_wave_plot.setXRange(-10,0)
        self.data_to_plot_alpha_high = np.empty((self.chunk_size+1,2))
        self.ptr_3 = 0
        self.curves_3 = []
        self.alpha_high_wave_plot.plotItem.plot()
        self.alpha_high_wave.addWidget(self.alpha_high_wave_plot)     
        # beta_low
        self.beta_low_wave_plot = pg.PlotWidget(title="Low")
        self.beta_low_wave_plot.setXRange(-10,0)
        self.data_to_plot_beta_low = np.empty((self.chunk_size+1,2))
        self.ptr_4 = 0
        self.curves_4 = []
        self.beta_low_wave_plot.plotItem.plot()
        self.beta_low_wave.addWidget(self.beta_low_wave_plot)     
        # beta_high
        self.beta_high_wave_plot = pg.PlotWidget(title="High")
        self.beta_high_wave_plot.setXRange(-10,0)
        self.data_to_plot_beta_high = np.empty((self.chunk_size+1,2))
        self.ptr_5 = 0
        self.curves_5 = []
        self.beta_high_wave_plot.plotItem.plot()
        self.beta_high_wave.addWidget(self.beta_high_wave_plot)     
        # gamma_low
        self.gamma_low_wave_plot = pg.PlotWidget(title="Low")
        self.gamma_low_wave_plot.setXRange(-10,0)
        self.data_to_plot_gamma_low = np.empty((self.chunk_size+1,2))
        self.ptr_6 = 0
        self.curves_6 = []
        self.gamma_low_wave_plot.plotItem.plot()
        self.gamma_low_wave.addWidget(self.gamma_low_wave_plot)     
        # gamma_mid
        self.gamma_mid_wave_plot = pg.PlotWidget(title="Mid")
        self.gamma_mid_wave_plot.setXRange(-10,0)
        self.data_to_plot_gamma_mid = np.empty((self.chunk_size+1,2))
        self.ptr_7 = 0
        self.curves_7 = []
        self.gamma_mid_wave_plot.plotItem.plot()
        self.gamma_mid_wave.addWidget(self.gamma_mid_wave_plot)     
        # attention
        self.attention_wave_plot = pg.PlotWidget()
        self.attention_wave_plot.setXRange(-10,0)
        self.data_to_plot_attention = np.empty((self.chunk_size+1,2))
        self.ptr_8 = 0
        self.curves_8 = []
        self.attention_wave_plot.plotItem.plot()
        self.attention_wave.addWidget(self.attention_wave_plot)     
        # meditation
        self.meditation_wave_plot = pg.PlotWidget()
        self.meditation_wave_plot.setXRange(-10,0)
        self.data_to_plot_meditation = np.empty((self.chunk_size+1,2))
        self.ptr_9 = 0
        self.curves_9 = []
        self.meditation_wave_plot.plotItem.plot()
        self.meditation_wave.addWidget(self.meditation_wave_plot)     
        # rawdata
        self.rawdata_wave_plot = pg.PlotWidget()
        self.rawdata_wave_plot.setXRange(-10,0)
        self.data_to_plot_rawdata = np.empty((self.chunk_size+1,2))
        self.ptr_10 = 0
        self.curves_10 = []
        self.rawdata_wave_plot.plotItem.plot()
        self.rawdata_wave.addWidget(self.rawdata_wave_plot)     

    def update_delta(self,delta):
        self.now = pg.ptime.time()
        for self.c_0 in self.curves_0:
            self.c_0.setPos(-(self.now-self.start_time),0)

        self.c_0 = self.ptr_0 % self.chunk_size
        if self.c_0 == 0:
            self.curve_0 = self.delta_wave_plot.plot()
            self.curves_0.append(self.curve_0)
            self.last_0 = self.data_to_plot_delta[-1]
            self.data_to_plot_delta = np.empty((self.chunk_size+1,2))
            self.data_to_plot_delta[0] = self.last_0
            while len(self.curves_0) > self.max_chunks:
                self.c_0 = self.curves_0.pop(0)
                self.delta_wave_plot.removeItem(self.c_0)
        else:
            self.curve_0 = self.curves_0[-1]
        self.data_to_plot_delta[self.c_0+1,0] = self.now - self.start_time
        self.data_to_plot_delta[self.c_0+1,1] = delta
        self.curve_0.setData(x=self.data_to_plot_delta[:self.c_0+2,0], y=self.data_to_plot_delta[:self.c_0+2,1])
        self.ptr_0 += 1

    def update_theta(self,theta):
        self.now = pg.ptime.time()
        for self.c_1 in self.curves_1:
            self.c_1.setPos(-(self.now-self.start_time),0)

        self.c_1 = self.ptr_1 % self.chunk_size
        if self.c_1 == 0:
            self.curve_1 = self.theta_wave_plot.plot()
            self.curves_1.append(self.curve_1)
            self.last_1 = self.data_to_plot_theta[-1]
            self.data_to_plot_theta = np.empty((self.chunk_size+1,2))
            self.data_to_plot_theta[0] = self.last_1
            while len(self.curves_1) > self.max_chunks:
                self.c_1 = self.curves_1.pop(0)
                self.theta_wave_plot.removeItem(self.c_1)
        else:
            self.curve_1 = self.curves_1[-1]
        self.data_to_plot_theta[self.c_1+1,0] = self.now - self.start_time
        self.data_to_plot_theta[self.c_1+1,1] = theta
        self.curve_1.setData(x=self.data_to_plot_theta[:self.c_1+2,0], y=self.data_to_plot_theta[:self.c_1+2,1])
        self.ptr_1 += 1

    def update_alpha_low(self,alpha_low):
        self.now = pg.ptime.time()
        for self.c_2 in self.curves_2:
            self.c_2.setPos(-(self.now-self.start_time),0)

        self.c_2 = self.ptr_2 % self.chunk_size
        if self.c_2 == 0:
            self.curve_2 = self.alpha_low_wave_plot.plot()
            self.curves_2.append(self.curve_2)
            self.last_2 = self.data_to_plot_alpha_low[-1]
            self.data_to_plot_alpha_low = np.empty((self.chunk_size+1,2))
            self.data_to_plot_alpha_low[0] = self.last_2
            while len(self.curves_2) > self.max_chunks:
                self.c_2 = self.curves_2.pop(0)
                self.alpha_low_wave_plot.removeItem(self.c_2)
        else:
            self.curve_2 = self.curves_2[-1]
        self.data_to_plot_alpha_low[self.c_2+1,0] = self.now - self.start_time
        self.data_to_plot_alpha_low[self.c_2+1,1] = alpha_low
        self.curve_2.setData(x=self.data_to_plot_alpha_low[:self.c_2+2,0], y=self.data_to_plot_alpha_low[:self.c_2+2,1])
        self.ptr_2 += 1

    def update_alpha_high(self,alpha_high):
        self.now = pg.ptime.time()
        for self.c_3 in self.curves_3:
            self.c_3.setPos(-(self.now-self.start_time),0)

        self.c_3 = self.ptr_3 % self.chunk_size
        if self.c_3 == 0:
            self.curve_3 = self.alpha_high_wave_plot.plot()
            self.curves_3.append(self.curve_3)
            self.last_3 = self.data_to_plot_alpha_high[-1]
            self.data_to_plot_alpha_high = np.empty((self.chunk_size+1,2))
            self.data_to_plot_alpha_high[0] = self.last_3
            while len(self.curves_3) > self.max_chunks:
                self.c_3 = self.curves_3.pop(0)
                self.alpha_high_wave_plot.removeItem(self.c_3)
        else:
            self.curve_3 = self.curves_3[-1]
        self.data_to_plot_alpha_high[self.c_3+1,0] = self.now - self.start_time
        self.data_to_plot_alpha_high[self.c_3+1,1] = alpha_high
        self.curve_3.setData(x=self.data_to_plot_alpha_high[:self.c_3+2,0], y=self.data_to_plot_alpha_high[:self.c_3+2,1])
        self.ptr_3 += 1


    def update_beta_low(self,beta_low):
        self.now = pg.ptime.time()
        for self.c_4 in self.curves_4:
            self.c_4.setPos(-(self.now-self.start_time),0)

        self.c_4 = self.ptr_4 % self.chunk_size
        if self.c_4 == 0:
            self.curve_4 = self.beta_low_wave_plot.plot()
            self.curves_4.append(self.curve_4)
            self.last_4 = self.data_to_plot_beta_low[-1]
            self.data_to_plot_beta_low = np.empty((self.chunk_size+1,2))
            self.data_to_plot_beta_low[0] = self.last_4
            while len(self.curves_4) > self.max_chunks:
                self.c_4 = self.curves_4.pop(0)
                self.beta_low_wave_plot.removeItem(self.c_4)
        else:
            self.curve_4 = self.curves_4[-1]
        self.data_to_plot_beta_low[self.c_4+1,0] = self.now - self.start_time
        self.data_to_plot_beta_low[self.c_4+1,1] = beta_low
        self.curve_4.setData(x=self.data_to_plot_beta_low[:self.c_4+2,0], y=self.data_to_plot_beta_low[:self.c_4+2,1])
        self.ptr_4 += 1

    def update_beta_high(self,beta_high):
        self.now = pg.ptime.time()
        for self.c_5 in self.curves_5:
            self.c_5.setPos(-(self.now-self.start_time),0)

        self.c_5 = self.ptr_5 % self.chunk_size
        if self.c_5 == 0:
            self.curve_5 = self.beta_high_wave_plot.plot()
            self.curves_5.append(self.curve_5)
            self.last_5 = self.data_to_plot_beta_high[-1]
            self.data_to_plot_beta_high = np.empty((self.chunk_size+1,2))
            self.data_to_plot_beta_high[0] = self.last_5
            while len(self.curves_5) > self.max_chunks:
                self.c_5 = self.curves_5.pop(0)
                self.beta_high_wave_plot.removeItem(self.c_5)
        else:
            self.curve_5 = self.curves_5[-1]
        self.data_to_plot_beta_high[self.c_5+1,0] = self.now - self.start_time
        self.data_to_plot_beta_high[self.c_5+1,1] = beta_high
        self.curve_5.setData(x=self.data_to_plot_beta_high[:self.c_5+2,0], y=self.data_to_plot_beta_high[:self.c_5+2,1])
        self.ptr_5 += 1

    def update_gamma_low(self,gamma_low):
        self.now = pg.ptime.time()
        for self.c_6 in self.curves_6:
            self.c_6.setPos(-(self.now-self.start_time),0)

        self.c_6 = self.ptr_6 % self.chunk_size
        if self.c_6 == 0:
            self.curve_6 = self.gamma_low_wave_plot.plot()
            self.curves_6.append(self.curve_6)
            self.last_6 = self.data_to_plot_gamma_low[-1]
            self.data_to_plot_gamma_low = np.empty((self.chunk_size+1,2))
            self.data_to_plot_gamma_low[0] = self.last_6
            while len(self.curves_6) > self.max_chunks:
                self.c_6 = self.curves_6.pop(0)
                self.gamma_low_wave_plot.removeItem(self.c_6)
        else:
            self.curve_6 = self.curves_6[-1]
        self.data_to_plot_gamma_low[self.c_6+1,0] = self.now - self.start_time
        self.data_to_plot_gamma_low[self.c_6+1,1] = gamma_low
        self.curve_6.setData(x=self.data_to_plot_gamma_low[:self.c_6+2,0], y=self.data_to_plot_gamma_low[:self.c_6+2,1])
        self.ptr_6 += 1

    def update_gamma_mid(self,gamma_mid):
        self.now = pg.ptime.time()
        for self.c_7 in self.curves_7:
            self.c_7.setPos(-(self.now-self.start_time),0)

        self.c_7 = self.ptr_7 % self.chunk_size
        if self.c_7 == 0:
            self.curve_7 = self.gamma_mid_wave_plot.plot()
            self.curves_7.append(self.curve_7)
            self.last_7 = self.data_to_plot_gamma_mid[-1]
            self.data_to_plot_gamma_mid = np.empty((self.chunk_size+1,2))
            self.data_to_plot_gamma_mid[0] = self.last_7
            while len(self.curves_7) > self.max_chunks:
                self.c_7 = self.curves_7.pop(0)
                self.gamma_mid_wave_plot.removeItem(self.c_7)
        else:
            self.curve_7 = self.curves_7[-1]
        self.data_to_plot_gamma_mid[self.c_7+1,0] = self.now - self.start_time
        self.data_to_plot_gamma_mid[self.c_7+1,1] = gamma_mid
        self.curve_7.setData(x=self.data_to_plot_gamma_mid[:self.c_7+2,0], y=self.data_to_plot_gamma_mid[:self.c_7+2,1])
        self.ptr_7 += 1

    def update_attention(self,attention):
        self.now = pg.ptime.time()
        for self.c_8 in self.curves_8:
            self.c_8.setPos(-(self.now-self.start_time),0)

        self.c_8 = self.ptr_8 % self.chunk_size
        if self.c_8 == 0:
            self.curve_8 = self.attention_wave_plot.plot()
            self.curves_8.append(self.curve_8)
            self.last_8 = self.data_to_plot_attention[-1]
            self.data_to_plot_attention = np.empty((self.chunk_size+1,2))
            self.data_to_plot_attention[0] = self.last_8
            while len(self.curves_8) > self.max_chunks:
                self.c_8 = self.curves_8.pop(0)
                self.attention_wave_plot.removeItem(self.c_8)
        else:
            self.curve_8 = self.curves_8[-1]
        self.data_to_plot_attention[self.c_8+1,0] = self.now - self.start_time
        self.data_to_plot_attention[self.c_8+1,1] = attention
        self.curve_8.setData(x=self.data_to_plot_attention[:self.c_8+2,0], y=self.data_to_plot_attention[:self.c_8+2,1])
        self.ptr_8 += 1

    def update_meditation(self,meditation):
        self.now = pg.ptime.time()
        for self.c_9 in self.curves_9:
            self.c_9.setPos(-(self.now-self.start_time),0)

        self.c_9 = self.ptr_9 % self.chunk_size
        if self.c_9 == 0:
            self.curve_9 = self.meditation_wave_plot.plot()
            self.curves_9.append(self.curve_9)
            self.last_9 = self.data_to_plot_meditation[-1]
            self.data_to_plot_meditation = np.empty((self.chunk_size+1,2))
            self.data_to_plot_meditation[0] = self.last_9
            while len(self.curves_9) > self.max_chunks:
                self.c_9 = self.curves_9.pop(0)
                self.meditation_wave_plot.removeItem(self.c_9)
        else:
            self.curve_9 = self.curves_9[-1]
        self.data_to_plot_meditation[self.c_9+1,0] = self.now - self.start_time
        self.data_to_plot_meditation[self.c_9+1,1] = meditation
        self.curve_9.setData(x=self.data_to_plot_meditation[:self.c_9+2,0], y=self.data_to_plot_meditation[:self.c_9+2,1])
        self.ptr_9 += 1

    def update_rawdata(self,rawdata):
        self.now = pg.ptime.time()
        for self.c_10 in self.curves_10:
            self.c_10.setPos(-(self.now-self.start_time),0)

        self.c_10 = self.ptr_10 % self.chunk_size
        if self.c_10 == 0:
            self.curve_10 = self.rawdata_wave_plot.plot()
            self.curves_10.append(self.curve_10)
            self.last_10 = self.data_to_plot_rawdata[-1]
            self.data_to_plot_rawdata = np.empty((self.chunk_size+1,2))
            self.data_to_plot_rawdata[0] = self.last_10
            while len(self.curves_10) > self.max_chunks:
                self.c_10 = self.curves_10.pop(0)
                self.rawdata_wave_plot.removeItem(self.c_10)
        else:
            self.curve_10 = self.curves_10[-1]
        self.data_to_plot_rawdata[self.c_10+1,0] = self.now - self.start_time
        self.data_to_plot_rawdata[self.c_10+1,1] = rawdata
        self.curve_10.setData(x=self.data_to_plot_rawdata[:self.c_10+2,0], y=self.data_to_plot_rawdata[:self.c_10+2,1])
        self.ptr_10 += 1

    def update_text(self,message_list):
        self.delta_data.setText(str(message_list[0]))
        self.update_delta(message_list[0])
        self.theta_data.setText(str(message_list[1]))
        self.update_theta(message_list[1])
        self.alpha_low_data.setText(str(message_list[2]))
        self.update_alpha_low(message_list[2])
        self.alpha_high_data.setText(str(message_list[3]))
        self.update_alpha_high(message_list[3])
        self.beta_low_data.setText(str(message_list[4]))
        self.update_beta_low(message_list[4])
        self.beta_high_data.setText(str(message_list[5]))
        self.update_beta_high(message_list[5])
        self.gamma_low_data.setText(str(message_list[6]))
        self.update_gamma_low(message_list[6])
        self.gamma_mid_data.setText(str(message_list[7]))
        self.update_gamma_mid(message_list[7])
        self.attention_data.setText(str(message_list[8]))
        self.update_attention(message_list[8])
        self.meditation_data.setText(str(message_list[9]))
        self.update_meditation(message_list[9])
        self.raw_data.setText(str(message_list[10]))
        self.update_rawdata(message_list[10])
    
    def run_thread(self):
        self.serial_message = SerialMessage(self)
        self.serial_message.start()
        self.serial_message.msg_signal.connect(self.update_text)

class SerialMessage(QThread):

    msg_signal = pyqtSignal(list)

    def __init__(self, headless=False):
        super(self.__class__, self).__init__()
        # self.port = "/dev/ttyUSB0"
        # self.ser = serial.Serial(self.port, 9600, timeout = None)
        self.data = []
        # print("Connected to", self.port)
    
    def run(self):
        while True:
            self.data = q.get()
            logging.info("Received Data: {}".format(self.data))
            # print(self.data)
            self.process_message_stream()            

    def process_message_stream(self):
        self.line = self.data
        
        if len(self.line) > 2:
            # print(self.line)
            self.msg_signal.emit(self.line)

def NeuroSky_reader(q):
    record = NeuroPy(port="/dev/tty.MindWaveMobile-SerialPo-1", queue = q)
    logging.info("Start to recording the data .... ")
    record.start()

if __name__ == '__main__':
    
    t1 = threading.Thread(target=NeuroSky_reader, args=(q,))
    t1.start()
    main(MainWindow)