import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import *


from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QMessageBox

myApp = QApplication(sys.argv)                   # Create an PyQT4 application object.
w = QWidget()                                    # The QWidget widget is the base class
w.setWindowTitle('Title Message')
w.resize(400, 200)

# ------------------------------------------
# -- Create textbox
# ------------------------------------------
myTextbox = QLineEdit(w)
myTextbox.move(20, 20)
myTextbox.resize(360,40)

# ------------------------------------------
# -- Create a button in the window
# ------------------------------------------
# myButton = QPushButton('Click1', w)
# myButton.move(20,80)
# myButton2 = QPushButton('Click2', w)
# myButton2.move(100, 80)
# myButton3 = QPushButton('Exit', w)
# myButton3.move(180, 80)
myButton4 = QPushButton('Send', w)
myButton4.move(260, 80)


# ------------------------------------------
# -- Create the actions
# ------------------------------------------
# @pyqtSlot()
# def on_click():
#     myTextbox.setText("Button-1 clicked.")
#
# @pyqtSlot()
# def on_click2():
#     myTextbox.setText("Button-2 clicked.")
#
# @pyqtSlot()
# def on_click3():                                 # Close window
#     w.close()

@pyqtSlot()
def on_click4():
    result = QMessageBox.question(w, 'Message', "Do you like?",
                                  QMessageBox.Yes | QMessageBox.No)
    if result == QMessageBox.Yes:
        myTextbox.setText("Clicked Yes on msgbox")
    else:
        myTextbox.setText("Clicked No on msgbox")


# ------------------------------------------
# -- Connect the signals to the slots
# ------------------------------------------
# myButton.clicked.connect(on_click)
# myButton2.clicked.connect(on_click2)
# myButton3.clicked.connect(on_click3)
myButton4.clicked.connect(on_click4)

# ------------------------------------------
# -- Show the window and run the app
# ------------------------------------------
w.show()
myApp.exec_()

