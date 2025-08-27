#!/usr/bin/env python3
from common import *
logger = get_logger("services_status")
import subprocess



method = "lines"
param = 10


def check_service(service_name,method,param):

	if method not in [ "lines","since" ]:
		print("method: " + method + " is unknown")	
		return { "color" : "red", "status" : "unknown", "log" : [ ] }

	report = { }

	result = subprocess.run(["systemctl", "is-active",service_name], capture_output=True, text=True)

	output = result.stdout
	error = result.stderr
	exit_code = result.returncode
	
	status = output.strip()

	report["status"] = status
	if status == "active":
		report["color"] = "green"
	else:
		report["color"] = "red"

	if method == "lines":
		p1 = "-n"
		if report["color"] != "green":
			param += 15
		p2 = str(param)
	elif method == "since":
		p1 = "--since"
		p2 = str(param) + "min ago"

	result = subprocess.run(["journalctl", "-u",service_name,p1,p2 ], capture_output=True, text=True)

	output = result.stdout
	error = result.stderr
	exit_code = result.returncode

	lines = output.strip().split("\n")
	report["log"] = lines
	
	return report

def check_all_services():

	
	all_services = { }	
	all_services["list"] = [ ]
	all_services["colors"] = { }
	all_services["services"] = { }
	

	section_name = "services"
	services = config[section_name].keys()
	for service in services:
		is_active = config.getboolean(section_name,service)
		if is_active:
			report = check_service(service,method,param)
			color = report["color"]
			if color not in all_services["colors"]:
				all_services["colors"][color] = [ ]
			all_services["colors"][color].append(service)
			all_services["list"].append(service)
			all_services["services"][service] = report

			
	return all_services

if __name__ == "__main__":
	report = check_all_services()
	pprint(report)
