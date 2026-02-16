import pwd, status, os, utils, compatibility, atexit, subprocess

def _getAllUsers():
	return [user.pw_name for user in pwd.getpwall()]

def _initUser():
	status.info("Initializing the shaweelMacro system user")
	users = _getAllUsers()
	shaweelMacroUserExistance = "shaweelMacro" in users
	status.info(f"Existance of the shaweelMacro system user: {shaweelMacroUserExistance}")
	if not shaweelMacroUserExistance:
		status.info("Creating the shaweelMacro system user")
		utils.alternativeCommands("useradd -r -s -m /bin/bash shaweelMacro",
			     "adduser --system --home /home/shaweelMacro --shell /bin/bash shaweelMacro",
			     "you must manually create a system account(UID < 1000) with a home directory and the shell at /bin/bash")
	status.info("Creating the home and cache directories if they don't exist yet and making the shaweelMacro system user own them")
	os.makedirs("/home/shaweelMacro/.cache", exist_ok=True)
	os.system("sudo chown -R shaweelMacro:shaweelMacro /home/shaweelMacro")
	os.system("sudo chown -R shaweelMacro:shaweelMacro /home/shaweelMacro/.cache")
	status.info("Adding the shaweelMacro system user to the video group")
	os.system("sudo usermod -aG video shaweelMacro")
	status.info('Setting password of the shaweelMacro system user to "shaweelMacro"')
	os.system("echo 'shaweelMacro:shaweelMacro' | sudo chpasswd")
	status.info("The shaweelMacro system user is ready for use")

def _initEnvironment():
	status.info("Initializing the RDP environment with a virtual screen and the Openbox window manager")
	displayNumber = utils.getFirstFreeDisplay()
	status.info(f"Creating virtual screen at :{displayNumber} for the shaweelMacro system user")
	xvfb = subprocess.Popen(f"sudo -u shaweelMacro LIBGL_ALWAYS_SOFTWARE=1 Xvfb :{displayNumber} -screen 0 1536x864x16", shell=True)
	atexit.register(lambda: xvfb.terminate())
	env = {
		"HOME": "/home/shaweelMacro",
		"DISPLAY": f":{displayNumber}",
		"XDG_RUNTIME_DIR": "/tmp",
		"DBUS_SESSION_BUS_ADDRESS": ""
	}

	status.info(f"Starting Openbox at screen :{displayNumber} for the shaweelMacro system user")
	openbox = subprocess.Popen(f"sudo -u shaweelMacro openbox-session", shell=True, env=env)
	atexit.register(lambda: openbox.terminate())
	status.info("The RDP environment is ready to use")

def _startRDPServices():
	status.info("Starting the xrdp service")
	utils.startService("xrdp")
	status.info("Checking for the xrdp-sesman service")
	if compatibility.checkService("xrdp-sesman"):
		status.info("The xrdp-sesman service has been found, enabling it")
		utils.startService("xrdp-sesman")
	else:
		status.warn("xrdp-sesman doesn't exist, this usually shouldn't be a problem")


def startRDP():
	pass

def stopRDP():
	pass

def init():
	status.info("Initializing RDP")
	_initUser()
	_initEnvironment()
	_startRDPServices()
	status.info("RDP is ready for use")

