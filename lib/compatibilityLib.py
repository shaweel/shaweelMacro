import lib.status as status, sys, os, shutil, pathlib

DEPENDENCY_LIST = ["xrdp", "pkill", "pkexec", "xfreerdp3", "chpasswd"]
OS = sys.platform
ROOT = os.geteuid() == 0
PATH_TO_FILE = pathlib.Path(__file__).parent.resolve()

def checkSystem():
	if OS != "linux":
		status.fatal("Incompatible operating system.")
	if not ROOT:
		status.fatal("shaweelMacro must be run as root")
	status.success("Your system is compatible with shaweelMacro")
def checkDependencies():
	missingDependencies = []
	for dependency in DEPENDENCY_LIST:
		if shutil.which(dependency): continue
		status.error(f"Missing system dependency: {dependency}")
		missingDependencies.append(dependency)
	if missingDependencies == []: 
		status.success("Your system has all the dependencies needed to run shaweelMacro")
		return
	status.fatal(f"""There are system dependencies that are missing, you must install all of them before being able to use shaweelMacro
Missing system dependencies: {", ".join(missingDependencies)}""")

def fullCheck():
	checkSystem()
	checkDependencies()
