from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import serial
import sys


import random, string


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.query = QLineEdit()
        self.query.setPlaceholderText("Search...")
        self.query.textChanged.connect(self.search)

        n_rows = 50
        n_cols = 4

        self.table = QTableWidget()
        self.table.setRowCount(n_rows)
        self.table.setColumnCount(n_cols)

        for c in range(0, n_cols):
            for r in range(0, n_rows):
                s = ''.join(random.choice(string.ascii_lowercase) for n in range(10))
                i = QTableWidgetItem(s)
                self.table.setItem(c, r, i)

        layout = QVBoxLayout()

        layout.addWidget(self.query)
        layout.addWidget(self.table)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

    def search(self, s):
        items = self.table.findItems(s, Qt.MatchContains)
        if items:  # we have found something
            item = items[0]  # take the first
            self.table.setCurrentItem(item)

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()

    app.exec_()