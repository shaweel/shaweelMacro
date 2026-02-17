import shutil, os, status, subprocess

def alternativeCommands(*commands, solution = None):
	baseCommands = []

	for command in commands:
		baseCommand = command.split()[0]
		baseCommands.append(baseCommand)
		if not shutil.which(baseCommand): continue
		os.system(command)
		return
	if not solution:
		status.fatal("None of the following shell commands were found: [], at least one of those must be installed on your system before using shaweelMacro")
	else:
		status.fatal(f"None of the following shell commands were found: [], to use shaweelMacro, {solution}")



def startService(service):
	init = getInitSystem()
	if init == "systemd":
		os.system(f"systemctl enable --now {service}")
	elif init == "runit":
		os.system(f"sv up {service} && ln -s /etc/runit/sv/{service} /etc/runit/runsvdir/default/")
	elif init == "openrc-init":
		os.system(f"rc-update add {service} && rc-service {service} start")
	else:
		status.fatal("You cannot use shaweelMacro on a system without systemd, runit or openrc-init")
	alternativeCommands(f"systemctl enable --now {service}",
			   f"rc-update add {service} && rc-service {service} start"
			   )
	
def getInitSystem():
	try:
		with open("/proc/1/comm") as f:
			init = f.read().strip()
	except:
		return None
	
	return init

def getFirstFreeDisplay():
	for i in range(0, 9223372036854775807):
		if os.path.exists(f"/tmp/.X{i}-lock"): continue
		status.info(f"Detected display :{i} as free")
		return i
	status.fatal("How the fuck do you have integer limit X servers running?")