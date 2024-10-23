#!/usr/bin/env python
## used to parse files more easily
#from __future__ import with_statement
import time
#
from pylab import *
# os
import os, time
# Numpy module
import numpy as np
# for command-line arguments
import sys
# Qt4 bindings for core Qt functionalities (non-GUI)
from PyQt5 import QtCore
# Python Qt4 bindings for GUI objects
from PyQt5 import QtWidgets as QtGui
from PyQt5.QtWidgets import QMessageBox
# import the MainWindow widget from the converted .ui files
from bernoulliGUI import Ui_MplMainWindow
import serial


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
class DesignerMainWindow(QtGui.QMainWindow, Ui_MplMainWindow):
  """Customization for Qt Designer created window"""
  def __init__(self, parent = None):
    # initialization of the superclass
    super(DesignerMainWindow, self).__init__(parent)
    # setup the GUI --> function generated by pyuic4
    self.setupUi(self)
    # Get initial parameters 
    self.tacq = float( self.lineEdit_displayTime.text()   ) 
    self.tavg = float( self.lineEdit_AveragingTime.text() )
    self.P    = []
    self.Q    = [] 
    self.tQ    = []
    self.tP    = []
    self.tinit = time.time()
    self.Qavg = 0 
    self.Pavg = 0 
    # Prepare plot 
    self.mpl.canvas.ax1.set_title( 'Flow rate (L/min)' )
    self.mpl.canvas.ax1.set_xlabel('Time (s)')
    self.mpl.canvas.ax2.set_xlabel('Time (s)')
    self.mpl.canvas.ax2.set_title( 'Pressure difference (mbar)' ) 
    self.hQ, = self.mpl.canvas.ax1.plot( self.tQ, self.Q, '-b')  
    self.hP, = self.mpl.canvas.ax2.plot( self.tP, self.P, '-g')  
    self.textQ = self.mpl.canvas.ax1.text(0.1, 0.9, f'Flow rate: {self.Qavg} L/min', transform=self.mpl.canvas.ax1.transAxes)
    self.textP = self.mpl.canvas.ax2.text(0.1, 0.9, f'Pressure: {self.Pavg} mbar', transform=self.mpl.canvas.ax2.transAxes)

    # Set up the serial connection (adjust 'COM3' to your port and baudrate if necessary)
    self.ser = serial.Serial('ttyUSB0', 9600)  # Replace 'COM3' with the correct port for your Arduino
    while True:
        try:
            # Read the serial data as a string
            line = self.ser.readline().decode('utf-8').strip()
            
            # Parse the data based on known format
            if line.startswith('Flow'):
                flow_value = int(line.split()[1])  # Extract the flow rate value
                self.Q.append(flow_value)               # Add to flow data array
                self.tQ.append(time.time() - self.tinit) # Add to time array 
                
            elif line.startswith('Pressure'):
                pressure_value = int(line.split()[1])  # Extract the pressure value
                self.P.append(pressure_value)   # Add to pressure data array
                self.tP.append(time.time() - self.tinit) # Add to time array 
                
        except Exception as e:
            print(f"Error reading serial data: {e}")

        # Update plots 
        self.hQ.set_data( self.tQ, self.Q )
        self.hP.set_data( self.tP, self.P )
        self.ax1.relim() 
        self.ax2.relim() 
        self.mpl.canvas.draw()
        sleep(0.01)

        # Perform average calculation
        if self.tQ[-1] - self.tQ[0]> self.tavg:
            self.Qavg = mean( self.Q[self.tQ>self.tQ[-1]-self.tavg] ) 
        if self.tP[-1] - self.tP[0]> self.tavg:
            self.Pavg = mean( self.P[self.tP>self.tP[-1]-self.tavg] ) 


# create the GUI application
app = QtGui.QApplication(sys.argv)
# instantiate the main window
dmw = DesignerMainWindow()
# show it
dmw.show()
# start the Qt main loop execution, exiting from this script
# with the same return code of Qt application
sys.exit(app.exec_())
