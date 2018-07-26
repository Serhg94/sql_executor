from PyQt5.QtWidgets import QApplication
import sys

import BdView
import TableModel
import SQLExecutor

app = QApplication(sys.argv)
model = TableModel.TableModel()
window = BdView.BdView(model)
controller = SQLExecutor.SQLExecutor()

window.initQueryExec.connect(controller.execQuery)
controller.executingBegan.connect(window.showWaitingSpinner)
controller.executingEnded.connect(window.showQueryResult)
controller.resultsObtained.connect(model.setData)

window.setConnToolTip(controller.getCapabilites())

sys.exit(app.exec_())

