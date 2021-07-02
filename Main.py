import PyQt5.QtWidgets as qtwid

class MainWindow(qtwid.QMainWindow):
    def __init__(self):
        super().__init__()
        self.te_query = qtwid.QTextEdit(self)
        self.btn_confirm = qtwid.QPushButton("확인",self)
        self.lb_query = qtwid.QLabel("[입력 문자열]",self)
        self.Initialize()
        
    def Initialize(self):
        self.setWindowTitle("Button 클릭하면 TextEdit에 입력 내용을 Label에 표시")
        self.resize(600,180)
        self.te_query.move(20,20)
        self.te_query.resize(300,40)
        self.btn_confirm.move(340,20)
        self.btn_confirm.resize(100,40)
        self.lb_query.move(20,100)
        self.lb_query.resize(600,40)
        self.btn_confirm.clicked.connect(self.Btn_confirmClick)

    def Btn_confirmClick(self):
        query = self.te_query.toPlainText()
        self.te_query.setText("")
        self.lb_query.setText(query)
        
    def uart(self):
        


if __name__ == "__main__":
    app = qtwid.QApplication(sys.argv) 
    mw = MainWindow() 
    mw.show() 
    app.exec_()


