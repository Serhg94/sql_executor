from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant, pyqtSignal


class TableModel(QAbstractTableModel):

    askForFetchMore = pyqtSignal()

    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self.__data = list()
        self.__hidden_data = list()
        self.__can_fetch_more = False

    def setData(self, column_description, data):
        self.__data = data
        self.__hidden_data = list()
        self.__can_fetch_more = False
        self.__column_description = column_description
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()

    def iCanFetchMore(self, data):
        self.__hidden_data = data
        self.__can_fetch_more = True

    def canFetchMore(self, index):
        return True if len(self.__hidden_data) > 0 else False

    def fetchMore(self, index):
        """
        add hidden data into model and ask for more
        :param index:
        :return:
        """
        self.__can_fetch_more = False
        self.beginInsertRows(QModelIndex(), len(self.__data), len(self.__data) + len(self.__hidden_data)-1)
        self.__data.extend(self.__hidden_data)
        self.__hidden_data = list()
        self.endInsertRows()
        self.askForFetchMore.emit()

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == Qt.DisplayRole:
            if Qt_Orientation == Qt.Horizontal:
                return str(self.__column_description[p_int][0])
            else:
                return str(p_int)
        return QVariant()

    def rowCount(self, parent):
        return len(self.__data)

    def columnCount(self, parent):
        if len(self.__data):
            return len(self.__data[0])
        else:
            return 0

    def data(self, idx=QModelIndex(), role=None):
        if role == Qt.DisplayRole:
            return str(self.__data[idx.row()][idx.column()])
        return QVariant()