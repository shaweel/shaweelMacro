import subprocess, pathlib, sys
PATH_TO_FILE = pathlib.Path(__file__).parent.resolve()

args = sys.argv
del args[0]

subprocess.run(f"cd {PATH_TO_FILE}", shell=True)
subprocess.run("python -m venv shaweelMacroVirtualEnvironment", shell=True)
subprocess.run("shaweelMacroVirtualEnvironment/bin/pip install -q -U pip colorama pyside6", shell=True)
subprocess.run(f"{PATH_TO_FILE}/shaweelMacroVirtualEnvironment/bin/python {PATH_TO_FILE}/main.py {" ".join(args)}", shell=True)