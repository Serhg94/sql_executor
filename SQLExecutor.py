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
        self.__current_conn_string = ''
        self.__conn = None
        self.__new_task = None
        self.__task_exist = threading.Event()
        self.__work_flag = threading.Event()
        self.__work_flag.set()
        self.__exec_thread = threading.Thread(target=self.__execProc)
        self.__exec_thread.start()

    def getCapabilites(self):
        """
        :return: string with description of all possible dialects
        """
        desc = ''
        for driver in Dialect.db_modules:
            desc = desc + Dialect.db_modules[driver]['description'] + '\n'
        return desc

    def stop(self):
        """
        stop working thread
        :return:
        """
        self.__work_flag.clear()
        self.__task_exist.set()
        self.__exec_thread.join()

    def __dropCurrConn(self):
        """
        close current connection, force reconnect next time
        :return:
        """
        if self.__conn is not None:
            try:
                self.__conn.close()
            except: pass
        self.__conn = None
        self.__current_conn_string = ''

    def __establishConnection(self, conn_string):
        """
        Parse connection string and create connection
        :param conn_string:
        :return:
        """
        url = Url.make_url(conn_string)
        self.__dropCurrConn()
        db = Dialect(url.drivername)
        if db.initModule() is None:
            raise Exception('driver for %s not found!' % url.drivername)
        self.__conn = db.connect(**url.translate_connect_args())
        self.__current_conn_string = conn_string

    def __doRequest(self, query):
        """
        execute query on self.__conn and emit signal with taked data
        :param query:
        :return: status string
        """
        cursor = self.__conn.cursor()
        cursor.execute(query)
        try:
            data = cursor.fetchall()
        except:
            data = None
        if data is not None and cursor.description is not None:
            """If nothing to fetch or description is empty -> query wasn`t DQL, but request was successful -> 
                                answer is OK"""
            self.resultsObtained.emit(cursor.description, data)
            return ''
        else:
            return  'OK'

    def __execProc(self):
        """
        Await task and try to process query: connect to db and do request
        :param query:
        :return:
        """
        while True:
            self.__task_exist.wait()
            if not self.__work_flag.is_set():
                return
            try:
                """if connection string has changed - establish connection again """
                if self.__new_task[0] != self.__current_conn_string:
                    self.__establishConnection(self.__new_task[0])
            except Exception as err:
                status_string = 'Connecting error: %s' % str(err) if str(err) else err.__class__.__name__
            else:
                """if connecting is successful - do request"""
                try:
                    status_string = self.__doRequest(self.__new_task[1])
                except Exception as err:
                    """if request failed - rollback"""
                    status_string = 'Execut error: %s' % str(err) if str(err) else err.__class__.__name__
                    try:
                        self.__conn.rollback()
                    except:
                        self.__dropCurrConn()
                else:
                    """if request is successful - commit changes"""
                    try:
                        self.__conn.commit()
                    except:
                        self.__dropCurrConn()
            self.executingEnded.emit(status_string)
            self.__task_exist.clear()

    def execQuery(self, conn_string, query):
        """
        create new task if work thread is`t busy
        :param conn_string: if rfc1738 format
        :param query:
        :return:
        """
        if self.__task_exist.is_set():
            return
        self.executingBegan.emit()
        self.__new_task = (conn_string, query)
        self.__task_exist.set()