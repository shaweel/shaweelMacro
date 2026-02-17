import utils, subprocess, status, os
DISPLAY = utils.getFirstFreeDisplay()

env = {"DISPLAY": f":{DISPLAY}"}

def startXephyr():
	status.info(f"Starting a 1536x864 Xephyr instance at :{DISPLAY}")
	return subprocess.Popen(f"Xephyr -br -ac -noreset -screen 1536x864 :{DISPLAY}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), DISPLAY
	
def runInXephyr(command, silent=True):
	status.info(f"Command executed in Xephyr instance at :{DISPLAY}: {command}")
	if silent:
		subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
	else:
		subprocess.Popen(command, shell=True, env=env)

def getXephyrRunning():
	return os.path.exists(f"/tmp/.X{DISPLAY}-lock")