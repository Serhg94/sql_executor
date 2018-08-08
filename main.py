from PyQt5.QtWidgets import QApplication
import sys

import BdView
import TableModel
import SQLExecutor

app = QApplication(sys.argv)
model = TableModel.TableModel()
view = BdView.BdView(model)
controller = SQLExecutor.SQLExecutor()

view.closing.connect(controller.stop)
view.initQueryExec.connect(controller.execQuery)
controller.executingBegan.connect(view.showWaitingSpinner)
controller.executingEnded.connect(view.showQueryResult)
controller.resultsObtained.connect(model.setData)
controller.youCanFetchMore.connect(model.iCanFetchMore)
model.askForFetchMore.connect(controller.fetchMore)

view.setConnToolTip(controller.getCapabilites())

sys.exit(app.exec_())

