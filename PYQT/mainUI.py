import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from background import MainWindow
import xlwt as xlwt
from PyQt5.QtGui import QBrush, QFont, QPixmap, QColor
from PyQt5.QtWidgets import *
import serial, random, string, sys, secrets
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtGui, QtCore
import threading, time
import qdarkstyle
import csv, sys
import pandas as pd

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Background")

        self.comboxbutton = QPushButton("Select")

        # self.comboxbutton.clicked.connect(combo)
        self.query = QLineEdit()
        self.query.setPlaceholderText("Search...")

        self.query.textChanged.connect(self.search)

        n_cols = 7
        self.table = QTableWidget()

        self.table.setColumnCount(n_cols)

        layout = QVBoxLayout()

        layout.addWidget(self.query)
        layout.addWidget(self.table)

        window = QWidget()
        window.setLayout((layout))
        self.setCentralWidget(QtWidgets.QMainWindow)

    def search(self, s): # 검색기능 함수
        items = self.table.findItems(s, Qt.MatchContains)
        if items:
            item = items[0]
            self.table.setCurrentItem(item)





app = QtWidgets.QApplication(sys.argv)
window = Window()
sys.exit(app.exec())