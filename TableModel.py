from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant


class TableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self.__data = list()

    def setData(self, column_description, data):
        self.__data = data
        self.__column_description = column_description
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()

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