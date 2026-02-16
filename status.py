import colorama as _colorama

_colorama.init()

def info(message):
	print(f"{_colorama.Fore.CYAN}[INFO] {_colorama.Fore.RESET}{message}")

def warn(message):
	print(f"{_colorama.Fore.YELLOW}[WARNING] {_colorama.Fore.RESET}{message}")

def error(message):
	print(f"{_colorama.Fore.RED}[ERROR] {_colorama.Fore.RESET}{message}")

def fatal(message):
	print(f"{_colorama.Fore.RED}[FATAL] {_colorama.Fore.RESET}{message}")
	exit()