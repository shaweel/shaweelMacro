from PySide6 import QtCore, QtWidgets, QtGui
import pwd, os, themes.assets_rc
import lib.configLib as configLib, lib.xrdpLib as xrdpLib, lib.status as status, lib.utils as utils, lib.compatibilityLib as compatibilityLib
import lib.signals as signals
os.environ["QT_LOGGING_TO_CONSOLE"] = "0"
os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.warning=false"
compatibilityLib.fullCheck()
app = QtWidgets.QApplication([])

fatalErrorWidth = 750
fatalErrorHeight = 300
fatalErrors = 0

def getAllSoberInstalls():
	allUsers = pwd.getpwall()
	allHomeDirectories = []
	for user in allUsers:
		if user.pw_name.startswith("shaweelMacroXrdp"): continue
		if not os.path.isdir(user.pw_dir): continue
		allHomeDirectories.append(user.pw_dir)
	
	allSoberDirectories = []
	for homeDirectory in allHomeDirectories:
		soberDirectory = f"{homeDirectory}/.var/app/org.vinegarhq.Sober"
		if not os.path.isdir(soberDirectory): continue
		allSoberDirectories.append(soberDirectory)
	return allSoberDirectories

class Welcome(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.themes = utils.getAllThemes()
		self.titleFont = QtGui.QFont()
		self.titleFont.setPointSize(16)
		self.smallFont = QtGui.QFont()
		self.smallFont.setPointSize(10)

		self.title = QtWidgets.QLabel(text="Welcome to shaweelMacro", alignment=QtCore.Qt.AlignCenter, font=self.titleFont)

		self.subTitle = QtWidgets.QLabel(text="Please set these basic settings below", alignment=QtCore.Qt.AlignCenter, wordWrap=True)

		self.themeText = QtWidgets.QLabel(text="Theme")

		self.theme = QtWidgets.QComboBox()
		
		for themeName in sorted(self.themes.keys()):
			self.theme.addItem(themeName)

		themeName = configLib.getFromConfig("theme")
		self.theme.currentTextChanged.connect(self.changeTheme)
		self.theme.setCurrentText(themeName)
		with open (self.themes[themeName], "r") as file:
			app.setStyleSheet(file.read())

		self.theme.setItemDelegate(QtWidgets.QStyledItemDelegate(self.theme))

		self.soberText = QtWidgets.QLabel(text="Sober installation directory")
		self.sober = QtWidgets.QListWidget()
		self.sober.addItems(getAllSoberInstalls())
		self.sober.addItem("Create a custom one")
		soberDirectory = configLib.getFromConfig("soberDirectory")
		self.sober.itemSelectionChanged.connect(self.changeSoberDirectory)
		try:
			self.sober.setCurrentItem(self.sober.findItems(soberDirectory, QtCore.Qt.MatchExactly)[0])
		except:
			status.error("Configuration contains a nonexistant value for the Sober installation directory, using the default.")
			self.sober.setCurrentItem(self.sober.findItems("Create a custom one", QtCore.Qt.MatchExactly)[0])
		self.soberCustomText = QtWidgets.QLabel(text="Creating a custom Sober installation directory will require you to login to Roblox again." \
		" Selecting a directory will just copy it's Roblox settings and accounts.", wordWrap=True, font=self.smallFont)

		self.startButton = QtWidgets.QPushButton("Start")
		self.startButton.released.connect(self.startRoblox)
		self.selectionContainer = QtWidgets.QWidget()
		self.selectionLayout = QtWidgets.QVBoxLayout(self.selectionContainer)
		self.selectionLayout.setSpacing(0)
		self.selectionLayout.setContentsMargins(0, 0, 0, 0)
		self.selectionLayout.addWidget(self.sober)
		self.selectionLayout.addWidget(self.soberCustomText)
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.addWidget(self.title)
		self.layout.addWidget(self.subTitle)
		self.layout.addWidget(self.themeText)
		self.layout.addWidget(self.theme)
		self.layout.addWidget(self.soberText)
		self.layout.addWidget(self.selectionContainer)
		self.layout.addWidget(self.startButton)
		self.layout.addStretch()
	def changeSoberDirectory(self):
		configLib.writeToConfig("soberDirectory", self.sober.currentItem().text())
		configLib.saveConfigToFile()
	def changeTheme(self, themeName):
		configLib.writeToConfig("theme", themeName)
		configLib.saveConfigToFile()
		with open (self.themes[themeName], "r") as file:
			app.setStyleSheet(file.read())
	def startRoblox(self):
		directory = self.sober.currentItem().text()
		self.startButton.setEnabled(False)
		self.startButton.setText("Running...")
		status.info("Starting roblox")
		self.soberThread = QtCore.QThread()
		self.soberThread.started.connect(lambda: [xrdpLib.startRoblox(directory), self.soberThread.quit()])
		self.soberThread.finished.connect(self.stopRoblox)
		self.soberThread.start()
	def stopRoblox(self):
		status.info("Roblox stopped")
		self.startButton.setEnabled(True)
		self.startButton.setText("Start")
		self.soberThread.deleteLater()
	def closeEvent(self, event):
		status.info("Main window closed, exiting program")
		exit()

currentFatalError = "Placeholder error message"

class FatalError(QtWidgets.QDialog):
	offsetPosition = QtCore.QPoint(0, 0)
	offsetNumber = 30
	def __init__(self):
		super().__init__()
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.titleFont = QtGui.QFont()
		self.titleFont.setPointSize(16)
		self.errorFont = QtGui.QFont("Monospace")
		self.errorFont.setPointSize(10)

		self.title = QtWidgets.QLabel(text="Fatal error", alignment=QtCore.Qt.AlignCenter, font=self.titleFont)
		self.subtitle = QtWidgets.QLabel(text="A fatal error has occured, forcing the application to quit:", wordWrap=True)
		self.text = QtWidgets.QTextEdit()
		self.text.setPlainText(currentFatalError)
		self.text.setFont(self.errorFont)
		self.text.setReadOnly(True)

		self.closeButton = QtWidgets.QPushButton(text="Close")
		self.closeButton.released.connect(self.reject)
		
		self.textContainer = QtWidgets.QWidget()
		self.textLayout = QtWidgets.QVBoxLayout(self.textContainer)
		self.textLayout.setSpacing(2)
		self.textLayout.setContentsMargins(0, 0, 0, 0)
		self.textLayout.addWidget(self.title)
		self.textLayout.addWidget(self.subtitle)
		self.textLayout.addWidget(self.text)
		self.textLayout.addStretch()
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.addWidget(self.textContainer)
		self.layout.addWidget(self.closeButton)
		self.setModal(True)
	def closeEvent(self, event):
		global fatalErrors
		fatalErrors -= 1
		if fatalErrors > 0:
			event.accept()
		else:
			exit()
	def reject(self):
		self.close()

def showWelcome():
	global welcomeWidget
	welcomeWidget = Welcome()
	welcomeWidget.setFixedSize(650, 400)
	welcomeWidget.setWindowTitle("shaweelMacro")
	welcomeWidget.show()

def showFatalError(errorMessage):
	global currentFatalError, fatalErrors
	currentFatalError = errorMessage
	fatalErrorWidget = FatalError()
	fatalErrors += 1
	fatalErrorWidget.setFixedSize(fatalErrorWidth, fatalErrorHeight)
	fatalErrorWidget.setWindowTitle("shaweelMacro")
	fatalErrorWidget.exec()

signals.signals.showWelcome.connect(showWelcome)
signals.signals.showFatalError.connect(showFatalError)

signals.showWelcome()

for error in status.getPreAppFatalErrors():
	signals.showFatalError(error)

app.exec()