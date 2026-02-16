import status, sys, os, shutil, subprocess, utils

DEPENDENCY_LIST = ["xrdp", "sudo", "echo", "chpasswd", "chown", "chmod"]
OS = sys.platform
ROOT = os.geteuid() == 0

def checkSystem():
	if OS != "linux":
		status.fatal("Incompatible operating system.")
	if not ROOT:
		status.fatal("shaweelMacro must be run as root")
	status.info("Your system is compatible with shaweelMacro")

def checkDependencies():
	missingDependencies = False
	for dependency in DEPENDENCY_LIST:
		if shutil.which(dependency): continue
		status.error(f"Missing system dependency: {dependency}")
		missingDependencies = True
	if not missingDependencies: 
		status.info("Your system has all the dependencies needed to run shaweelMacro")
		return
	status.fatal("There are system dependencies that are missing, you must install all of them before being able to use shaweelMacro")

def checkService(service):
	init = utils.getInitSystem()
	if init == "systemd":
		result = subprocess.run(["systemctl", "status", f"{service}.service"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		return result.returncode == 0
	elif init == "runit":
		return os.path.exists(f"/etc/sv/{service}") or os.path.exists(f"/etc/runit/sv/{service}")
	elif init == "openrc-init":
		return os.path.exists(f"/etc/init.d/{service}")
	else:
		status.fatal("You cannot use shaweelMacro on a system without systemd, runit or openrc-init")