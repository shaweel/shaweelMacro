import colorama, os, sys, lib.configLib as configLib, lib.utils as utils, lib.signals as signals
from PySide6.QtCore import QTimer
from PySide6 import QtWidgets

preAppFatalErrors = []

colorama.init()

def info(message):
	print(f"{colorama.Fore.CYAN}[INFO] {colorama.Fore.RESET}{message}")

def warn(message):
	print(f"{colorama.Fore.YELLOW}[WARNING] {colorama.Fore.RESET}{message}")

def error(message):
	print(f"{colorama.Fore.RED}[ERROR] {colorama.Fore.RESET}{message}")

def success(message):
	print(f"{colorama.Fore.GREEN}[SUCCESS] {colorama.Fore.RESET}{message}")

def fatal(message):
	print(f"{colorama.Fore.RED}[FATAL] {colorama.Fore.RESET}{message}")
	ignoreFatal = False
	try:
		if sys.argv[1] == "--ignore-fatal": ignoreFatal = True
	except:
		pass
	if ignoreFatal == True: return
	if QtWidgets.QApplication.instance() is not None:
		signals.showFatalError(message)
	else:
		global preAppFatalErrors
		preAppFatalErrors.append(message)

def getPreAppFatalErrors():
    return preAppFatalErrors