import sys
import logging

from PyQt5.QtWidgets import *
from PyQt5 import uic


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class LogStringHandler(logging.Handler):

    def __init__(self, target_widget):
        super(LogStringHandler, self).__init__()
        self.target_widget = target_widget

    def emit(self, record):
        self.target_widget.append(record.asctime + ' -- ' + record.getMessage())

class TestWindow(QMainWindow, test_ui_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        logger = logging.getLogger()
        logger.addHandler(LogStringHandler(self.testTextBrowser))

        # 이벤트 연결
        self.testButton.clicked.connect(self.clicked_test_button)

    def clicked_test_button(self):
        message_alert = self.test_logging()
        QMessageBox.about(self, 'testButton 눌림 알람', message_alert)

    def test_logging(self):
        total_repeat_count = int(self.countTempDummy.text() if self.countTempDummy.text() != '' else 0)
        if total_repeat_count <= 0:
            return '출력 대상이 없음'
        for i in range(0, total_repeat_count):
            logging.error('Error %s ' % i)
            logging.info('Info %s ' % i)
            logging.warning('Warning %s ' % i)
            logging.debug('Debug %s ' % i)
        return '로그 출력 완료'


if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_window = TestWindow()
    test_window.show()
    app.exec_()