import colorama as _colorama
import os, sys

_colorama.init()

def info(message):
	print(f"{_colorama.Fore.CYAN}[INFO] {_colorama.Fore.RESET}{message}")

def warn(message):
	print(f"{_colorama.Fore.YELLOW}[WARNING] {_colorama.Fore.RESET}{message}")

def error(message):
	print(f"{_colorama.Fore.RED}[ERROR] {_colorama.Fore.RESET}{message}")

def success(message):
	print(f"{_colorama.Fore.GREEN}[SUCCESS] {_colorama.Fore.RESET}{message}")

def fatal(message):
	print(f"{_colorama.Fore.RED}[FATAL] {_colorama.Fore.RESET}{message}")
	try:
		if sys.argv[1] != "--ignore-fatal": os._exit(0)
	except:
		os._exit(0)
