from PyQt5.QtCore import QObject, pyqtSignal

import Url


class SQLExecutor(QObject):

    executingBegan = pyqtSignal()
    resultsObtained = pyqtSignal(list)
    executingEnded = pyqtSignal(str)


    def __init__(self, parent=None):
        super(SQLExecutor, self).__init__(parent)

    def getCapabilites(self):
        return """
        sqlite,
        
        """

    def execQuery(self, conn_string, query):
        try:
            url = Url.make_url(conn_string)
            print(url.database)
            print(url.password)
            print(url.port)
            print(url.drivername)
            print(url.username)
            print(url.host)
        except Exception as e:
            self.executingEnded.emit(str(e))
        self.executingBegan.emit()
        data = eval(query)
        self.resultsObtained.emit(data)
        self.executingEnded.emit('')