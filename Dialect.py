import importlib


class Dialect:

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
        if self.__name in Dialect.db_modules:
            self.__db = importlib.import_module(Dialect.db_modules[self.__name]['package'])
        return self.__db

    def connect(self, **kwargs):
        if self.__name == 'sqlite':
            return self.__db.connect(database=kwargs['database'])
        elif self.__name == 'postgresql':
            return self.__db.connect(database=kwargs['database'], user=kwargs['user'], password=kwargs['password']
                                     , port=kwargs['port'], host=kwargs['host'])
        elif self.__name == 'oracle':
            return self.__db.connect(database=kwargs['database'], user=kwargs['user'], password=kwargs['password']
                                     , port=kwargs['port'], host=kwargs['host'])
        elif self.__name == 'mysql':
            return self.__db.connect(database=kwargs['database'], user=kwargs['user'], password=kwargs['password']
                                     , port=kwargs['port'], host=kwargs['host'])
        elif self.__name == 'mssql':
            return self.__db.connect(database=kwargs['database'], user=kwargs['user'], password=kwargs['password']
                                     , port=kwargs['port'], host=kwargs['host'])