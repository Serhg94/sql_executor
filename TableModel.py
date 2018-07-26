from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant


class TableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self.__data = list()

    def setData(self, data):
        self.__data = data
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()

    def rowCount(self, parent):
        return len(self.__data)

    def columnCount(self, parent):
        if len(self.__data):
            return len(self.__data[0])
        else:
            return 0

    def data(self, idx=QModelIndex(), role=None):
        if (role == Qt.DisplayRole):
            return self.__data[idx.row()][idx.column()]
        return QVariant()