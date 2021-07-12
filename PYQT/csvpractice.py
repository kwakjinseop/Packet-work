import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
import pandas as pd


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 700, 500
        self.resize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.button = QPushButton('&Export To Excel', clicked=self.exportToExcel)
        layout.addWidget(self.button)

        self.loadData()

    def exportToExcel(self):
        columnHeaders = []

        # create column header list
        for j in range(self.table.model().columnCount()):
            columnHeaders.append(self.table.horizontalHeaderItem(j).text())

        df = pd.DataFrame(columns=columnHeaders)

        # create dataframe object recordset
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                df.at[row, columnHeaders[col]] = self.table.item(row, col).text()

        df.to_excel('Dummy File XYZ.xlsx', index=False)
        print('Excel file exported')

    def loadData(self):
        self.headerLabels = list('ABCDEFG')

        n = 3000
        self.table.setRowCount(n)
        self.table.setColumnCount(len(self.headerLabels))
        self.table.setHorizontalHeaderLabels(self.headerLabels)

        for row in range(n):
            for col in range(len(self.headerLabels)):
                item = QTableWidgetItem('Cell {0}-{1}'.format(self.headerLabels[col], row + 1))
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 17px;
        }
    ''')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')