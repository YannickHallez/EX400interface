# Python Qt5 bindings for GUI objects
from PyQt5 import QtWidgets as QtGui
#from PyQt5.QtWidgets import QApplication, QWidget
# import the Qt4Agg FigureCanvas object, that binds Figure to
# Qt4Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt5agg \
import FigureCanvasQTAgg as FigureCanvas
# Matplotlib Figure object
from matplotlib.figure import Figure
class MplCanvas(FigureCanvas):
  """Class to represent the FigureCanvas widget"""
  def __init__(self):
    # setup Matplotlib Figure and Axis
    self.fig = Figure()
    self.ax1 = self.fig.add_subplot(121)
    self.ax2 = self.fig.add_subplot(122)
    # initialization of the canvas
    FigureCanvas.__init__(self, self.fig)
    # we define the widget as expandable
    FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    # notify the system of updated policy
    FigureCanvas.updateGeometry(self)
class MplWidget(QtGui.QWidget):
  """Widget defined in Qt Designer"""
  def __init__(self, parent = None):
    # initialization of Qt MainWindow widget
    QtGui.QWidget.__init__(self, parent)
    # set the canvas to the Matplotlib widget
    self.canvas = MplCanvas()
    # create a vertical box layout
    self.vbl = QtGui.QVBoxLayout()
    # add mpl widget to vertical box
    self.vbl.addWidget(self.canvas)
    # set the layout to the vertical box
    self.setLayout(self.vbl)

