from PySide6 import QtCore

class Signals(QtCore.QObject):
	showWelcome = QtCore.Signal()
	showFatalError = QtCore.Signal(str)

signals = Signals()

def showWelcome():
	signals.showWelcome.emit()
def showFatalError(errorMessage="Placeholder error message"):
	signals.showFatalError.emit(errorMessage)