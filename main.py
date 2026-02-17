import robloxManager, compatibility, json, os, status, atexit
DEFAULT_CONFIG = '{"linkCode": 0}'

try:
	CONFIG = json.loads(open("config.json").read())
except FileNotFoundError:
	file = open("config.json", "x")
	file.write(DEFAULT_CONFIG)
	CONFIG = json.loads(DEFAULT_CONFIG)

def startMacro():
	compatibility.checkSystem()
	compatibility.checkDependencies()
	xephyrInstance, display = robloxManager.startXephyr()
	atexit.register(lambda: xephyrInstance.terminate())

	while not robloxManager.getXephyrRunning():
		pass
	status.info(f"Xephyr has started at :{display}")
	robloxManager.runInXephyr("xterm")
	while robloxManager.getXephyrRunning():
    		pass


startMacro()