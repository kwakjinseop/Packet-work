from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
import csv


class MyTabs(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabmon = QWidget()
        self.tabtue = QWidget()

        # Add tabs
        self.tabs.addTab(self.tabmon, "Monday")
        self.tabs.addTab(self.tabtue, "Tuesday")

        #Save Button

        self.buttonSavemon = QtWidgets.QPushButton('Save', self)
        self.buttonSavemon.clicked.connect(self.handleSavemon)

        self.buttonSavetue = QtWidgets.QPushButton('Save', self)
        self.buttonSavetue.clicked.connect(self.handleSavetue)

        #Initiate Tables
        self.createTable()

        # Create Monday tab
        self.tabmon_layout = QVBoxLayout(self.tabmon)
        self.tabmon_layout.addWidget(self.tablewidgetmon)
        self.tabmon_layout.addWidget(self.buttonSavemon)

        # Create Tuesday tab
        self.tabtue_layout = QVBoxLayout(self.tabtue)
        self.tabtue_layout.addWidget(self.tablewidgettue)
        self.tabtue_layout.addWidget(self.buttonSavetue)

        # Add tabs to widget
        layout.addWidget(self.tabs)

    def createTable(self):
        #Monday Table
        self.tablewidgetmon = QTableWidget()
        self.tablewidgetmon.setRowCount(10)
        self.tablewidgetmon.setColumnCount(2)
        self.tablewidgetmon.setHorizontalHeaderLabels(["Time", "File Name"])

        #Tuesday Table
        self.tablewidgettue = QTableWidget()
        self.tablewidgettue.setRowCount(12)
        self.tablewidgettue.setColumnCount(2)
        self.tablewidgettue.setHorizontalHeaderLabels(["Time", "File Name"])


    def handleSavemon(self):
#        with open('monschedule.csv', 'wb') as stream:
        with open('monschedule.csv', 'w') as stream:                  # 'w'
            writer = csv.writer(stream, lineterminator='\n')          # + , lineterminator='\n'
            for row in range(self.tablewidgetmon.rowCount()):
                rowdata = []
                for column in range(self.tablewidgetmon.columnCount()):
                    item = self.tablewidgetmon.item(row, column)
                    if item is not None:
#                        rowdata.append(unicode(item.text()).encode('utf8'))
                        rowdata.append(item.text())                   # +
                    else:
                        rowdata.append('')

                writer.writerow(rowdata)


    def handleSavetue(self):
        with open('tueschedule.csv', "w") as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.tablewidgettue.rowCount()):
# +                
                fields = [
                    self.tablewidgettue.item(rowNumber, columnNumber).text() \
                            if self.tablewidgettue.item(rowNumber, columnNumber) is not None else ""
                    for columnNumber in range(self.tablewidgetmon.columnCount())
                ]                

                writer.writerow(fields)


def loadCsv(self):
    try:
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
        self.all_data = pd.read_csv(path)
    except:
        print(path)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = MyTabs()
    main.show()
    sys.exit(app.exec_()) 