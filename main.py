import xrdpLib, basicSettings, compatibility, json
DEFAULT_CONFIG = '{"linkCode": 0}'

try:
	CONFIG = json.loads(open("config.json").read())
except FileNotFoundError:
	file = open("config.json", "x")
	file.write(DEFAULT_CONFIG)
	CONFIG = json.loads(DEFAULT_CONFIG)

def startMacro():
	compatibility.fullCheck()
	basicSettings.showWindow()
	#xrdpLib.startRoblox()

startMacro()