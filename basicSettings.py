from PySide6 import QtCore, QtWidgets, QtGui
import sys, pwd, os, pathlib

PATH_TO_FILE = pathlib.Path(__file__).parent.resolve()

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

def getAllThemes():
	themes = {}
	for file in os.scandir(f"{PATH_TO_FILE}/themes"):
		if not file.is_file(): continue
		themes[file.name.replace(".qss", "")] = f"{PATH_TO_FILE}/themes/{file.name}"
	return themes

class BasicSettings(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.themes = getAllThemes()
		titleFont = QtGui.QFont()
		titleFont.setPointSize(16)
		self.title = QtWidgets.QLabel(text="Welcome to shaweelMacro", alignment=QtCore.Qt.AlignCenter, font=titleFont)

		self.subTitle = QtWidgets.QLabel(text="Please set these basic settings below", alignment=QtCore.Qt.AlignCenter, wordWrap=True)

		self.themeText = QtWidgets.QLabel(text="Theme")

		self.theme = QtWidgets.QComboBox()
		self.theme.currentTextChanged.connect(self.changeTheme)
		
		for themeName in sorted(self.themes.keys()):
			self.theme.addItem(themeName)

		self.theme.setCurrentText("Dark")

		self.soberText = QtWidgets.QLabel(text="Sober installation directory")
		self.sober = QtWidgets.QListWidget()
		self.sober.addItems(getAllSoberInstalls())
		self.sober.addItem("Create a custom one")	

		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.addWidget(self.title)
		self.layout.addWidget(self.subTitle)
		self.layout.addWidget(self.themeText)
		self.layout.addWidget(self.theme)
		self.layout.addWidget(self.soberText)
		self.layout.addWidget(self.sober)
		self.layout.addStretch()
	def changeTheme(self, themeName):
		with open (self.themes[themeName], "r") as file:
			self.setStyleSheet(file.read())


def showWindow():
	app = QtWidgets.QApplication([])
	widget = BasicSettings()
	widget.setFixedSize(550, 300)
	widget.setWindowTitle("shaweelMacro")
	widget.show()
	sys.exit(app.exec())