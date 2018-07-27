import importlib


class Dialect:
    """
    Implements different connect attrs for some DB-API2 connectors
    """

    db_modules = {
        'postgresql': {
            'package': 'psycopg2',
            'description': 'Conn for PostgreSQL: postgresql://scott:tiger@localhost/mydatabase'
        },
        'mysql': {
            'package': 'mysql.connector',
            'description': 'Conn for MySQL: mysql://scott:tiger@localhost/foo'
        },
        'oracle': {
            'package': 'cx_oracle',
            'description': 'Conn for Oracle: oracle://scott:tiger@127.0.0.1:1521/sidname'
        },
        'mssql': {
            'package': 'pyodbc',
            'description': 'Conn for MSSQL: mssql://scott:tiger@hostname:port/dbname'
        },
        'sqlite': {
            'package': 'sqlite3',
            'description': 'Conn for sqlite: sqlite:///C:\\path\\to\\foo.db'
        }
    }

    def __init__(self, name):
        self.__name = name
        self.__db = None

    def initModule(self):
        """
        Try to import python DB-API2 connector module
        :return: module
        """
        if self.__name in Dialect.db_modules:
            self.__db = importlib.import_module(Dialect.db_modules[self.__name]['package'])
        return self.__db

    def connect(self, **kwargs):
        """
        Process arguments from Url.translate_connect_args for connecting to DB
        :param kwargs: arguments from Url.translate_connect_args
        :return: connection object
        """
        if self.__name == 'sqlite':
            return self.__db.connect(database=kwargs['database'])
        elif self.__name == 'postgresql' or self.__name == 'mysql':
            kwargs['user'] = kwargs['username']
            del kwargs['username']
            return self.__db.connect(**kwargs)
        elif self.__name == 'oracle':
            dsn = self.__db.makedsn(kwargs['host'], str(kwargs['port']), kwargs['database'])
            return self.__db.connect(dsn=dsn, user=kwargs['username'], password=kwargs['password'])
        elif self.__name == 'mssql':
            conString = "DRIVER={SQL Server Native Client 11.0};SERVER=%s,%s;DATABASE=%s;UID=%s;PWD=%s" % (
                kwargs['host'], kwargs['port'], kwargs['database'], kwargs['username'], kwargs['password'])
            return self.__db.connect(conString)