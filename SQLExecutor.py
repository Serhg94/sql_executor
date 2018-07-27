from PyQt5.QtCore import QObject, pyqtSignal
import threading

import Url
from Dialect import Dialect


class SQLExecutor(QObject):

    executingBegan = pyqtSignal()
    resultsObtained = pyqtSignal(tuple, list)
    executingEnded = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SQLExecutor, self).__init__(parent)
        self.__exec_thread = None

    def getCapabilites(self):
        desc = ''
        for driver in Dialect.db_modules:
            desc = desc + Dialect.db_modules[driver]['description'] + '\n'
        return desc

    def __execQuery(self, url, query):
        conn = None
        try:
            db = Dialect(url.drivername)
            if db.initModule() is None:
                self.executingEnded.emit('ERROR: driver for %s not found!' % url.drivername)
                return
            conn = db.connect(**url.toDict())
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            self.resultsObtained.emit(cursor.description, data)
            self.executingEnded.emit('')
        except Exception as err:
            self.executingEnded.emit('ERROR: %s' % str(err))
            return
        else:
            conn.commit()
        finally:
            if conn is not None:
                conn.close()

    def execQuery(self, conn_string, query):
        if self.__exec_thread is not None and self.__exec_thread.is_alive():
            return
        self.executingBegan.emit()
        try:
            url = Url.make_url(conn_string)
        except Url.ArgumentError as err:
            self.executingEnded.emit('Wrong argument in connection string: %s' % str(err))
            return
        except Exception as err:
            self.executingEnded.emit('ERROR: %s' % str(err))
            return
        self.__exec_thread = threading.Thread(target=self.__execQuery, args=(url, query))
        self.__exec_thread.start()