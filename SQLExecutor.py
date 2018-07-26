from PyQt5.QtCore import QObject, pyqtSignal
import importlib
import threading

import Url


class SQLExecutor(QObject):

    executingBegan = pyqtSignal()
    resultsObtained = pyqtSignal(tuple, list)
    executingEnded = pyqtSignal(str)

    db_modules = {
        'postgresql': {
            'package': 'psycopg2',
            'conn_args': ('user', 'password', 'host', 'database'),
            'description': 'Conn for PostgreSQL: postgresql://scott:tiger@localhost/mydatabase'
        },
        'mysql': {
            'package': 'mysql.connector',
            'conn_args': ('user', 'password', 'host', 'database'),
            'description': 'Conn for MySQL: mysql://scott:tiger@localhost/foo'
        },
        'oracle': {
            'package': 'cx_oracle',
            'conn_args': ('user', 'password', 'host', 'database'),
            'description': 'Conn for Oracle: oracle://scott:tiger@127.0.0.1:1521/sidname'
        },
        'mssql': {
            'package': 'pyodbc',
            'conn_args': ('user', 'password', 'host', 'database'),
            'description': 'Conn for MSSQL: mssql://scott:tiger@hostname:port/dbname'
        },
        'sqlite': {
            'package': 'sqlite3',
            'conn_args': ('database',),
            'description': 'Conn for sqlite: sqlite:///C:\\path\\to\\foo.db'
        }
    }

    def __init__(self, parent=None):
        super(SQLExecutor, self).__init__(parent)
        self.__exec_thread = None

    def getCapabilites(self):
        desc = ''
        for driver in SQLExecutor.db_modules:
            desc = desc + SQLExecutor.db_modules[driver]['description'] + '\n'
        return desc

    def __execQuery(self, url, query):
        conn = None
        try:
            if url.drivername in SQLExecutor.db_modules:
                db = importlib.import_module(SQLExecutor.db_modules[url.drivername]['package'])
            else:
                self.executingEnded.emit('ERROR: driver for %s not found!' % url.drivername)
                return
            args = url.toDict()
            filtered_args = dict()
            for name in SQLExecutor.db_modules[url.drivername]['conn_args']:
                if name in args:
                    filtered_args[name] = args[name]
            conn = db.connect(**filtered_args)
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