import sys
import PyQt5.QtWidgets as qtwid
from MainWindow import MainWindow

app = qtwid.QApplication(sys.argv)
mw = MainWindow()
mw.show()
app.exec()