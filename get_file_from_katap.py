import json
import requests
import sys
import os
import time
import zipfile
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
katap_url = config['katap']['url']
katap_ip = config['katap']['ip']
katap_pass = config['katap']['password']
katap_user = config['katap']['username']

headersAuthPOST = {
		"Host": katap_ip,
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0",
		"Accept": "application/json, text/plain, */*",
		"Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
		"Accept-Encoding": "gzip, deflate, br",
		"Content-Type": "application/json;charset=utf-8",
		"Origin": "https://" + katap_ip,
		"Connection": "keep-alive",
		"Referer": "https://" + katap_ip + "/katap/",
		"DNT": "1",
		"Upgrade-Insecure-Requests": "1",
		"Pragma": "no-cache",
		"Cache-Control": "no-cache"
	}

headersAuthGET = {
		"Host": katap_ip,
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0",
		"Accept": "application/json, text/plain, */*",
		"Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
		"Accept-Encoding": "gzip, deflate, br",
		"Origin": "https://" + katap_ip,
		"Connection": "keep-alive",
		"Referer": "https://" + katap_ip + "/katap/",
		"Upgrade-Insecure-Requests": "1",
		"X-Slide-User-Session":"true",
		"X-Slide-User-Session":"0"
        }

def main():

	if(not get_file_by_hash(katap_ip, katap_user, katap_pass, katap_url)):
		return

def get_file_by_hash(katap_ip, username, password, katap_url):
	# get file by hash from katap

	session = requests.Session()
	
	# log in katap
	
	request = session.post(f"https://{katap_ip}/apt/api/userLogin", verify=False, headers=headersAuthPOST,
	json={"username":username,"password":password,"local":False})
	
	if('"success": true' in request.text):
		print("")
	else:
		print("login error")
		return False
  
	# MD5 hash is supported, maybe someting else

	hash = sys.argv[1]
  
  	# hash cleaning - optional
	
  	#hash = hash.replace("[{hash:",'')
	#hash = hash.replace("}]",'')
	
	# get file from katap
	
	request = session.get(f"https://{katap_url}:8443/apt/api/detectedFile?md5=" + hash, verify=False, headers=headersAuthGET)

	# if u want to sand file
	
	filename = hash + ".zip"
	file = open(filename,'wb')
	file.write(request.content) 
	
	# then u can send it to sandbox or attach to incident in IRP
	
main()
