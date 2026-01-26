import platform, os, status, webbrowser
OS = platform.system()

def _terminateAllRobloxInstanceWindows():
	os.system("TASKKILL /F /IM RobloxPlayerBeta.exe")

def _terminateAllRobloxInstancesLinux():
	pass #TODO Implement linux support

def terminateAllRobloxInstances():
	status.info("Terminating all Roblox instances.")
	if OS == "Windows": _terminateAllRobloxInstanceWindows()
	elif OS == "Linux": _terminateAllRobloxInstancesLinux()


def _joinPublicServer():
	status.info("Joining a public server because a private server link code wasn't provided in the configuration.")
	webbrowser.open("https://www.roblox.com/games/start?placeId=1537690962")

def _joinPrivateServer(linkCode):
	status.info(f"Joining private server with link code: {linkCode}")
	webbrowser.open(f"https://www.roblox.com/games/start?placeId=1537690962&?linkCode={linkCode}")


def _joinBeeSwarmSimulatorWindows(linkCode):
	status.info("Joining Bee Swarm Simulator.")
	if (linkCode == 0):
		_joinPublicServer()
		return
	_joinPrivateServer(linkCode)

def _startX11RDP():
	pass #TODO Make it launch a X11 RDP and somehow transfer the code to there idk how ill fucking to this shit, ts is gonna be complicated

def _joinBeeSwarmSimulatorInX11RDP():
	pass #TODO good luck future me

def joinBeeSwarmSimulator(linkCode=0):
	if OS == "Windows": _joinBeeSwarmSimulatorWindows()
	elif OS == "Linux": _startX11RDP()