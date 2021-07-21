# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FilterView.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import xlwt as xlwt
from PyQt5.QtGui import QBrush, QFont, QPixmap, QColor
from PyQt5.QtWidgets import *
import serial, random, string, sys, secrets
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtGui, QtCore
import qdarkstyle



class Ui_FilterView(object):
    def setupUi(self, FilterView):
        FilterView.setWindowTitle("FilterView")
        FilterView.resize(1081, 835)
        self.centralwidget = QtWidgets.QWidget(FilterView)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 451, 771))
        self.tableWidget.setRowCount(20000)
        self.tableWidget.setColumnCount(7)
        column_headers = ['Number', 'STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.tableWidget.setObjectName("tableWidget")
        #############왼쪽 테이블########################
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(480, 280, 111, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Number")
        self.comboBox.addItem("STX")
        self.comboBox.addItem("Time")
        self.comboBox.addItem("Checksum")
        self.comboBox.addItem("Reserved")
        self.comboBox.addItem("Length")
        self.comboBox.addItem("Payload")
        #############콤보박스##########################
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(480, 350, 111, 41))
        self.textEdit.setObjectName("textEdit")
        #############텍스트 입력상자#########################
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(480, 420, 111, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Apply")
        #############Apply 버튼###########################
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(610, 10, 451, 771))
        self.tableWidget_2.setRowCount(20000)
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setObjectName("tableWidget_2")
        column_headers = ['Number', 'STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']
        self.tableWidget_2.setHorizontalHeaderLabels(column_headers)
        ##############데이터 전송 부분###########################
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 710, 331, 51))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 710, 111, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Send")
        FilterView.setCentralWidget(self.centralwidget)












        #############오른쪽 테이블###############################
        FilterView.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(FilterView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1081, 26))
        self.menubar.setObjectName("menubar")
        self.menuFilterView = QtWidgets.QMenu(self.menubar)
        self.menuFilterView.setObjectName("menuFilterView")
        FilterView.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(FilterView)
        self.statusbar.setObjectName("statusbar")
        FilterView.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFilterView.menuAction())
        FilterView.show()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FilterView = QtWidgets.QMainWindow()
    ui = Ui_FilterView()
    ui.setupUi(FilterView)
    sys.exit(app.exec_())

