class main_window(QWidget):
    def __init__(self):
        super(main_window, self).__init__()
        def Calendar(self):
            self.cal = QCalendarWidget(self)
            self.cal.setGridVisible(True)
            vbox = QVBoxLayout()
            vbox.addWidget(self.cal)
            self.calGroup = QGroupBox(title='day')
            self.calGroup.setLayout(vbox)
            self.cal.clicked.connect(self.Calendar_click)
            def Calendar_click(self, date):
                global calendarDate calendarDate = date
                Tab1().ViewTable(date)
                calendarDate = QDate.toPyDate(date)
            def MotherInformation(self):
                vbox.addWidget(tabs)
                tabs.addTab(Tab1(), 'TAB1') # this value -> Class Tab1 ?? tabs.addTab(QPushButton(), 'TAB2') self.lineGroup1.setLayout(vbox) class Tab1(QWidget): def __init__(self): super(Tab1, self).__init__() self.ViewTable() def ViewTable(self, caldate): print(caldate) tab1TableWidget = QTableWidget() tab1TableWidget.resize(613,635) tab1TableWidget.horizontalHeader() tab1TableWidget.setRowCount(100) tab1TableWidget.setColumnCount(100)