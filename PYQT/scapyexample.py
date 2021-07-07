import PyQt5.QtWidgets as qtwid
import serial
import sys
import numpy as np
import random
import time
from PyQt5 import QtWidgets, QtCore, QtGui

value1 = 0


class EditableHeaderView(QtWidgets.QHeaderView):
    textChanged = QtCore.pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(EditableHeaderView, self).__init__(QtCore.Qt.Horizontal, parent)
        self._is_editable = dict()
        self.setSectionsClickable(True)
        self._lineedit = QtWidgets.QLineEdit(self, visible=False)
        self._lineedit.editingFinished.connect(self._lineedit.hide)
        self._lineedit.textChanged.connect(self.on_text_changed)
        self.sectionDoubleClicked.connect(self.on_sectionDoubleClicked)
        self._current_index = -1
        self._filters_text = dict()

    def setEditable(self, index, is_editable):
        if 0 <= index < self.count():
            self._is_editable[index] = is_editable

    @QtCore.pyqtSlot()
    def hide_lineedit(self):
        self._filters_text[self._current_index] = self._lineedit.text()
        self._lineedit.hide()
        self._current_index = -1
        self._lineedit.clear()

    @QtCore.pyqtSlot(int)
    def on_sectionDoubleClicked(self, index):
        self.hide_lineedit()
        is_editable = False
        if index in self._is_editable:
            is_editable = self._is_editable[index]
        if is_editable:
            geom = QtCore.QRect(self.sectionViewportPosition(index), 0, self.sectionSize(index), self.height())
            self._lineedit.setGeometry(geom)
            if index in self._filters_text:
                self._lineedit.setText(self._filters_text[index])
            self._lineedit.show()
            self._lineedit.setFocus()
            self._current_index = index
            self.textChanged.emit(self._current_index, self._lineedit.text())

    @QtCore.pyqtSlot(str)
    def on_text_changed(self, text):
        if self._current_index != -1:
            # self.model().setHeaderData(self._current_index, self.orientation(), text)
            self.textChanged.emit(self._current_index, text)


class MainWindow(qtwid.QMainWindow):

    def __init__(self):
        super().__init__()
        tableview = QtWidgets.QTableView()
        headerview = EditableHeaderView(tableview)
        tableview.setHorizontalHeader(headerview)
        model = QtGui.QStandardItemModel(20, 6, self)
        self._proxy = QtCore.QSortFilterProxyModel(self)
        self._proxy.setSourceModel(model)
        tableview.setModel(self._proxy)
        tableview.setSortingEnabled(True)

        # 원소대입 부분
        for i in range(model.rowCount()):
            for j in range(model.columnCount()):
                text = ''.join(random.sample(list("abcdefghijklmnopqrstuvwxyz"), 4))
                it = QtGui.QStandardItem(text)
                model.setItem(i, j, it)
        headerview.setEditable(2, True)
        headerview.setEditable(4, True)
        headerview.setEditable(7, True)
        headerview.textChanged.connect(self.on_text_changed)

        self.te_query = qtwid.QTextEdit(self)  # 문자열 입력부분
        self.btn_confirm = qtwid.QPushButton("확인", self)
        # self.lb_query = qtwid.QLabel("[입력 문자열]",self)
        self.tableWidget = qtwid.QTableWidget(self)

    def Initialize(self):
        self.setWindowTitle("Button 클릭하면 TextEdit에 입력 내용을 Label에 표시")

        self.setViewData()

        self.te_query.move(10, 510)  # 문자열 입력부분
        self.te_query.resize(300, 40)  # 문자열 입력부분
        self.btn_confirm.move(330, 510)  # 확인 버튼
        self.btn_confirm.resize(100, 40)  # 확인버튼
        # self.lb_query.move(20,100)
        # self.lb_query.resize(600,40)
        self.btn_confirm.clicked.connect(self.uart)

    def setViewData(self):
        column_headers = ['STX', 'Time', 'Checksum', 'Respond', 'Length', 'Payload']
        result_array = np.array(
            [0xab, 0x1c, 0x3b, 0xf3, 0x75, 0x46, 0x14, 0x28, 0xf2, 0xca, 0xb4, 0xe7, 0xd6, 0x08, 0x00, 0x44, 0x89, 0xaa,
             0xac, 0xff, 0xfa])

        # print(result_array[0:2])
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        self.tableWidget.setItem(value1, 0, qtwid.QTableWidgetItem(str(hex(result_array[0]))))  # STX
        self.tableWidget.setItem(value1, 1, qtwid.QTableWidgetItem(str(hex(sum(result_array[1:5])))))  # Time
        self.tableWidget.setItem(value1, 2, qtwid.QTableWidgetItem(str(hex(sum(result_array[5:9])))))  # Checksum
        self.tableWidget.setItem(value1, 3, qtwid.QTableWidgetItem(str(hex(sum(result_array[9:13])))))  # Respond
        self.tableWidget.setItem(value1, 4, qtwid.QTableWidgetItem(str(hex(sum(result_array[13:15])))))  # Length
        self.tableWidget.setItem(value1, 5, qtwid.QTableWidgetItem(str(hex(sum(result_array[15:21])))))  # Payload

    # def Btn_confirmClick(self):
    #     query = self.te_query.toPlainText()
    #     self.te_query.setText("")
    #     self.lb_query.setText(query)

    def uart(self):
        global value1
        query = self.te_query.toPlainText()
        ser = serial.Serial("COM3", 115200, timeout=1)
        # op = query
        op = b'ab 3b:f3:75:46:14:d8:f2:ca:b4:e7:d6:08:00'
        x = str(op)
        print(x)
        a = str(op.split(":")[0])
        # b = str(op.split(":")[1])
        # c = str(op.split(":")[2])
        # d = str(op.split(":")[3])
        # e = str(op.split(":")[4])
        # f = str(op.split(":")[5])
        #
        print(a)
        # print(b)
        # print(c)
        # print(d)
        # print(e)
        # print(f)

        ser.write(op.encode())  # 값 입력
        print("R:", ser.readline())
        str_data = str(ser.readline(), 'utf-8')
        # print(str_data)
        hex_int = int(str_data, 16)
        length = len(str_data)

        # self.tableWidget.setItem(value1, 1, qtwid.QTableWidgetItem(a)) #STX
        # self.tableWidget.setItem(value1, 2, qtwid.QTableWidgetItem(str(op.split(':')[1]))) #Time
        # self.tableWidget.setItem(value1, 3, qtwid.QTableWidgetItem(str(op.split(':')[2]))) #Checksum
        # self.tableWidget.setItem(value1, 4, qtwid.QTableWidgetItem(str(op.split(':')[3]))) #Respond
        # self.tableWidget.setItem(value1, 5, qtwid.QTableWidgetItem(str(op.split(':')[4]))) #Length
        # self.tableWidget.setItem(value1, 6, qtwid.QTableWidgetItem(time.strftime(str(op.split(':')[2])))) #Payload

        value1 = value1 + 1
        if op is 'q':
            ser.close()
        print(value1)
        print(len(str_data))

    def on_text_changed(self, col, text):
        self._proxy.setFilterKeyColumn(col)
        self._proxy.setFilterWildcard("*{}*".format(text) if text else "")


if __name__ == "__main__":
    app = qtwid.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec()




