import shutil, os, status, tkinter, subprocess, pwd, pam
from tkinter import simpledialog

def alternateCommands(*commands, solution = None):
	baseCommands = []

	for commandString in commands:
		baseCommand = commandString.split()[0]
		baseCommands.append(baseCommand)
		if not shutil.which(baseCommand): continue
		return command(commandString)
	if not solution:
		status.fatal(f"None of the following shell commands were found: {baseCommands}, at least one of those must be installed on your system before using shaweelMacro")
	else:
		status.fatal(f"None of the following shell commands were found: {baseCommands}, to use shaweelMacro, {solution}")

def command(command, ignoreReturnCode=False):
	status.info(f'Running the command "{command}"')
	process = subprocess.run(command, shell=True, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
	if process.returncode != 0 and not ignoreReturnCode:
		status.error(f'The command "{command}" ran into an error: {process.stderr}')


def getCommandOutput(command):
	process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return process.stdout, process.stderr

def getFirstFreeDisplay():
	for i in range(0, 9223372036854775807):
		if os.path.exists(f"/tmp/.X{i}-lock"): continue
		return i
	status.fatal("How the fuck do you have integer limit X servers running?")

def getServiceStatus(service):
	init = getInitSystem()
	if init == "systemd":
		result = subprocess.run(f"systemctl is-active {service}", shell=True, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
		if result == 0: result = True
		elif result == 3: result = False
		else: result = None
	elif init == "runit":
		result = subprocess.run(f"sv check {service}", shell=True, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
		if result == 0: result = True
		elif result == 1: result = False
		else: result = None
	elif init == "openrc-init":
		if result == 0: result = True
		elif result == 3: result = False
		else: result = None
		result = subprocess.run(f"rc-service {service} status", shell=True, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
	else: 
		status.fatal("You cannot use shaweelMacro on a system without systemd, runit or openrc-init")

	if result:
		status.info(f"Service {service} is active")
	else:
		status.info(f"Service {service} is inactive")
	return result

def enableService(service):
	status.info(f"Enabling service {service}")
	init = getInitSystem()
	if init == "systemd":
		command(f"systemctl enable {service}")
	elif init == "runit":
		command(f"ln -s /etc/runit/sv/{service} /etc/runit/runsvdir/default/")
	elif init == "openrc-init":
		command(f"rc-update add {service}")
	else:
		status.fatal("You cannot use shaweelMacro on a system without systemd, runit or openrc-init")

def startService(service):
	status.info(f"Starting service {service}")
	init = getInitSystem()
	if init == "systemd":
		command(f"systemctl start {service}")
	elif init == "runit":
		command(f"sv up {service}")
	elif init == "openrc-init":
		command(f"rc-service {service} start")
	else:
		status.fatal("You cannot use shaweelMacro on a system without systemd, runit or openrc-init")

def enableAndStartService(service):
	enableService(service)
	startService(service)
	
def getInitSystem():
	try:
		with open("/proc/1/comm") as f:
			init = f.read().strip()
	except:
		return None
	return init