import lib.utils as utils, lib.status as status, atexit, re, os, signal
from PySide6.QtCore import QEventLoop

displayNumber = utils.getFirstFreeDisplay()
os.environ["QT_LOGGING_TO_CONSOLE"] = "0"
os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.warning=false"
loop = QEventLoop()

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
	global xfreerdp3Process
	status.info(f"Starting the RDP session using xfreerdp3 at display :{displayNumber}")
	xfreerdp3Process = utils.popen(f"echo y | xfreerdp3 /v:127.0.0.1 /u:shaweelMacroXrdp{userNumber} /p:shaweelMacro")

def getRdpDisplay():
	output = utils.getCommandOutput(f"ps -u shaweelMacroXrdp{userNumber} -o pid,cmd")
	display_re = re.compile(r"Xorg\s+(:\d+)")
	for line in output:
		match = display_re.search(line)
		if match:
			return match.group(1)
	return None


def deleteXrdpUser():
	global userNumber
	if userNumber is None: return
	try:
		utils.command(f"umount -l /home/shaweelMacroXrdp{userNumber}/thinclient_drives", 
		ignoreReturnCode=True, crucial=False)
	except:
		pass
	utils.alternateCommands(f"userdel -r -f shaweelMacroXrdp{userNumber}",
	f"deluser --remove-home shaweelMacroXrdp-{userNumber}", crucial=False)

def getRdpRunning():
	return xfreerdp3Process.poll() is None


def command(commandToRun, ignoreReturnCode=False, crucial=True):
	return utils.command(f"DISPLAY=:{displayNumber} {commandToRun}", ignoreReturnCode, crucial)

def popen(commandToRun, ignoreReturnCode=False, crucial=True):
	return utils.popen(f"DISPLAY=:{displayNumber} {commandToRun}", ignoreReturnCode, crucial)

def removeDisplayLockFile():
	try:
		lock_file = f"/tmp/.X{displayNumber}-lock"
		if not os.path.exists(lock_file):
			status.info("Display lock file doesn't exist, this is a good thing")
		os.remove(lock_file)
		status.info(f"Removed display lock: {lock_file}")
	except:
		pass

def cleanUp():
	global xfreerdp3Process
	status.info("Attempting to perform exit cleanup")
	deleteXrdpUser()
	status.info("Attempting to remove the display lock file")
	removeDisplayLockFile()
	status.info("Killing PGID, have a nice day")
	os.killpg(os.getpgid(xfreerdp3Process.pid), signal.SIGKILL)

def startRoblox(soberDirectory):
	if soberDirectory != "Create a custom one":
		status.info(f"Attempting to start Sober while copying the {soberDirectory} directory")
	else:
		status.info(f"Attempting to start Sober while creating a custom directory")
	startXrdpServices()
	createXrdpUser()
	connectToXrdp()
	while not getRdpRunning():
		loop.processEvents()
	atexit.register(cleanUp)
	while getRdpRunning():
		loop.processEvents()
	
