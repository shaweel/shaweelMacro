import utils, status, atexit, subprocess, re

displayNumber = utils.getFirstFreeDisplay()

def startXrdpServices():
	xrdpStatus = utils.getServiceStatus("xrdp")
	xrdpSesmanStatus = utils.getServiceStatus("xrdp-sesman")
	if xrdpSesmanStatus == True and xrdpStatus == True: 
		status.success("All xrdp services are active, your computer can now be connected to via RDP")
		return

	if xrdpStatus == False: utils.startService("xrdp")
	elif xrdpStatus == None: status.fatal("The xrdp service is missing.")
	if xrdpSesmanStatus == False: utils.startService("xrdp-sesman")
	elif xrdpSesmanStatus == None: status.fatal("The xrdp-sesman service is missing.")

	failed = False
	if utils.getServiceStatus("xrdp") == False: 
		status.error("Failed to start the xrdp service")
		failed = True
	if utils.getServiceStatus("xrdp-sesman") == False: 
		status.error("Failed to start the xrdp-sesman service")
		failed = True
	if failed:
		status.fatal("One or more services have failed starting")
	status.success("All xrdp services are active, your computer can now be connected to via RDP")

def createXrdpUser():
	global userNumber
	users = utils.getAllUsers()
	userNumber = 0
	while True:
		if f"shaweelMacroXrdp{userNumber}" in users:
			userNumber += 1
		else: break

	utils.alternateCommands(f"useradd -m -r -s /bin/bash shaweelMacroXrdp{userNumber}",
	f"adduser --system --home /home/shaweelMacroXrdp{userNumber} --shell /bin/bash shaweelMacroXrdp{userNumber}",
	solution="you must manually create a system account(UID < 1000) with a home directory and the shell at /bin/bash")
	utils.command(f'echo "shaweelMacroXrdp{userNumber}:shaweelMacro" | chpasswd')

def connectToXrdp():
	xrdpProcess = subprocess.Popen(f"echo y | xfreerdp3 /v:127.0.0.1 /u:shaweelMacroXrdp{userNumber} /p:shaweelMacro"
		  , shell=True, text=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
	atexit.register(lambda: xrdpProcess.terminate())

def getRdpDisplay():
	output = utils.getCommandOutput(f"ps -u shaweelMacroXrdp{userNumber} -o pid,cmd")
	display_re = re.compile(r"Xorg\s+(:\d+)")
	for line in output:
		match = display_re.search(line)
		if match:
			return match.group(1)
	return None

def deleteXrdpUser():
	utils.alternateCommands(f"userdel -r -f shaweelMacroXrdp{userNumber}",
	f"deluser --remove-home shaweelMacroXrdp-{userNumber}")

def startRoblox():
	startXrdpServices()
	createXrdpUser()
	atexit.register(lambda: deleteXrdpUser())
	connectToXrdp()
	print(getRdpDisplay())
	while True:
		pass
	"""_startXephyr()
	_startOpenBox()
	_startRoblox()"""