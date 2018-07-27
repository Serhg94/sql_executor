from PyQt5.QtWidgets import QWidget, QTableView, QGridLayout, QLabel, QLineEdit, QTextEdit, QSplitter, QGroupBox\
    , QStackedWidget, QPushButton, QTextBrowser
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCloseEvent

import QtWaitingSpinner

class BdView(QWidget):

    initQueryExec = pyqtSignal(str, str)
    closing = pyqtSignal()

    def __init__(self, model, parent=None):
        super(BdView, self).__init__(parent)
        self.__model = model
        self.__initUI()
        self.__connect_slots()

    def closeEvent(self, event: QCloseEvent):
        self.closing.emit()

    def __initUI(self):
        self.__layout = QGridLayout(self)
        self.__layout.setSpacing(4)

        controls = QGroupBox()
        up_layout = QGridLayout()
        self.__table_view = QTableView()
        self.__connection_string = QLineEdit()
        self.__connection_string.setText('sqlite:///:memory:')
        self.__request_string = QTextEdit()
        self.__request_string.setPlaceholderText('Your query')
        self.__text_result_view = QTextBrowser()
        self.__text_result_view.setText('Write your first query')
        self.__exec_btn = QPushButton('Execute')
        self.__waiting_spinner = QtWaitingSpinner.QtWaitingSpinner()

        up_layout.addWidget(QLabel('Connection'), 1, 0)
        up_layout.addWidget(self.__connection_string, 1, 1)

        up_layout.addWidget(QLabel('SQL'), 2, 0)
        up_layout.addWidget(self.__request_string, 2, 1)

        up_layout.addWidget(self.__exec_btn, 1, 2, 2, 1)

        controls.setLayout(up_layout)

        self.__presentations = QStackedWidget()
        self.__presentations.addWidget(self.__table_view)
        self.__presentations.addWidget(self.__waiting_spinner)
        self.__presentations.addWidget(self.__text_result_view)
        self.__presentations.setCurrentWidget(self.__text_result_view)

        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)
        splitter.addWidget(controls)
        splitter.addWidget(self.__presentations)
        splitter.setSizes([200, 600])

        self.__layout.addWidget(splitter)

        self.__table_view.setModel(self.__model)
        self.setLayout(self.__layout)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('SQL executor')
        self.show()

    def __connect_slots(self):
        self.__exec_btn.pressed.connect(self.__execQuery)

    def __execQuery(self):
        self.initQueryExec.emit(self.__connection_string.text(), self.__request_string.toPlainText())

    def showWaitingSpinner(self):
        self.__presentations.setCurrentWidget(self.__waiting_spinner)
        self.__waiting_spinner.start()

    def showQueryResult(self, error):
        self.__waiting_spinner.stop()
        if error:
            self.__text_result_view.setText(error)
            self.__presentations.setCurrentWidget(self.__text_result_view)
        else:
            self.__presentations.setCurrentWidget(self.__table_view)

    def setConnToolTip(self, text):
        self.__connection_string.setToolTip(text)
