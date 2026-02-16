import os, pathlib, importlib.util
PATH_TO_FILE = pathlib.Path(__file__).parent.resolve()

os.system(f"cd {PATH_TO_FILE}")
os.system("python -m venv shaweelMacroVirtualEnvironment")
os.system("shaweelMacroVirtualEnvironment/bin/pip install -q -U pip")
os.system("shaweelMacroVirtualEnvironment/bin/pip install -q -U colorama")
os.system("shaweelMacroVirtualEnvironment/bin/python main.py")