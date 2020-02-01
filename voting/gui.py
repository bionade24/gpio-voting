from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel
from PyQt5 import uic, QtCore
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import os
import gpio


class GPIOThread(QtCore.QThread):
    
    button_clicked = QtCore.pyqtSignal(int, name='button_clicked')

    def __init__(self):
        super(GPIOThread, self).__init__()


    def __del__(self):
        self.wait()


    def run(self):
        self.button_clicked.emit(gpio.check_button_state())


class VotingUI(QWidget):

    def __init__(self, parent=None):
        super(VotingUI, self).__init__(parent)
        self.ui = uic.loadUi("VotingUI.ui", self)


class ResultsUI(pg.PlotWidget):

    def __init__(self, parent=None):
        super(ResultsUI, self).__init__(parent)
        self.options = [1, 2]
        dg = pg.BarGraphItem(x=self.options, height=self.votes, width=0.6, brush='r')
        self.addItem(dg)
        self.setLabel('bottom', '<h1><pre>Option1    Option2</pre></h1>')


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setFixedSize(500, 300)
        self.startVotingUI()
        self.votes = [0, 0]


    def startVotingUI(self):
        self.VotingUI = VotingUI(self)
        self.setWindowTitle("Abstimmung")
        self.setCentralWidget(self.VotingUI)
        #Start checking for GPIO signals
        self.gpiothread = GPIOThread()
        self.gpiothread.start()
        self.show()


    def startResultsUI(self):
        self.votes = [24, 35]
        self.ResultsUI = ResultsUI(self)
        self.setWindowTitle("Ergebnisse")
        self.setCentralWidget(self.ResultsUI)
        self.show()


    @QtCore.pyqtSlot(int, name='button_clicked')
    def button_clicked(self, i):
        self.votes[i] += 1
        self.startResultsUI()


def main(argv):
    app = QApplication(argv)
    main = MainWindow()
    main.setWindowTitle("Abstimmung Thema")
    main.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main(sys.argv)