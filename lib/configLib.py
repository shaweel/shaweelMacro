import json, inspect, lib.status as status
DEFAULT_CONFIG = {"linkCode": 0, "theme": "Dark", "soberDirectory": "Create a custom one"}
CONFIG = {}

def getFullConfig():
	return CONFIG

def getFromConfig(key):
	try:
		return getFullConfig()[key]
	except:
		try:
			defaultValue = DEFAULT_CONFIG[key]
			status.info(f"Key \"{key}\" doesn't yet have a value assigned. Using the default value: {defaultValue}")
			CONFIG[key] = defaultValue
			return defaultValue
		except:
			caller_info = inspect.getframeinfo(inspect.currentframe().f_back)
			filename = caller_info.filename
			function = caller_info.function
			line = caller_info.lineno
			status.fatal(f'Attempted to get nonexistent key "{key}": {filename}.{function}() line {line}')
			return None

def writeToConfig(key, value):
	CONFIG[key] = value

def saveConfigToFile():
	with open("config.json", "w") as file:
		file.write(json.dumps(CONFIG))

try:
	with open("config.json", "r") as file:
		CONFIG = json.loads(file.read())

except FileNotFoundError:
	status.info("Config file not found, creating")
	CONFIG = {}
	saveConfigToFile()
except json.JSONDecodeError:
	status.warn("Corrupted config file, resetting to the defaults")
	CONFIG = {}
	saveConfigToFile()



