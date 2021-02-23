#!/usr/bin/env python3

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import re
import yaml
import sys

def init():
	#load config from yaml file
	with open("config.yaml") as f:
		global CONFIG
		CONFIG = yaml.load(f, Loader=yaml.FullLoader)
	global s
	s = HTMLSession()

def login():
	#reads login info from json
	with open("login.json") as f:
		login = json.load(f)
		payload = {
			"UserName": login["user"],
			"Password": login["password"],
			"SAMLResponse": ""
		}
	#logs in
	p = s.post(CONFIG["url_login"], data=payload)

	#gets saml response from html
	soup = BeautifulSoup(p.content, "html.parser")
	value = ""
	try:
		value = soup.find("input", {"name": "SAMLResponse"}).get("value")
	except:
		pass
    
	#sends response to complete login
	r_payload = {"SAMLResponse": value}
	p = s.post(CONFIG["url_saml"], data=r_payload)
    
def getlist():
	#gets links and names from courses
	data = []

	#if json exists, load it
	try:
		with open("20-21/courses20-21.json", "r") as j:
			data = json.load(j)

	#if json doesn't exist, generate it from html source
	except FileNotFoundError:
		with open("20-21/list.html", "r") as f:
			soup = BeautifulSoup(f.read(), "html.parser")
		courses = []
		try:
			list = soup.find_all("a", class_="aalink")
			for item in list:
				name = re.search(">(.+)<", str(item)).group()[1:-1]
				link = re.split("\"", str(item))[3]
				courses.append({"name": name, "link": link})
		except:
			pass
		with open("20-21/courses20-21.json", "w") as f:
			f.write(json.dumps(courses))

		data = courses
	return data

def getname(link):
	page = s.get(link)
	soup = BeautifulSoup(page.content, "html.parser")
	name = re.search("<h1>(.+)</h1>", str(soup)).group()[4:-5]
	return name

def enroll(data):
	for item in data:
		try:
			page = s.get(item["link"])
			soup = BeautifulSoup(page.content, "html.parser")

			r_id = soup.find("input", {"name": "id"}).get("value")
			r_in = soup.find("input", {"name": "instance"}).get("value")
			r_sk = soup.find("input", {"name": "sesskey"}).get("value")
			r_qf_k = re.search("_qf__(.+)form", str(soup)).group()
			r_qf_v = soup.find("input", {"name": r_qf_k}).get("value")
			r_mf = soup.find("input", {"name": "mform_isexpanded_id_selfheader"}).get("value")

			payload = {
				"id": r_id,
				"instance": r_in,
				"sesskey": r_sk,
				r_qf_k: r_qf_v,
				"mform_isexpanded_id_selfheader": r_mf
			}

			p = s.post(CONFIG["url_enroll"], data=payload)
			print("Enrolled in: "+item["name"])
		except:
			print("Already enrolled in: "+item["name"])

def main():
	init()
	login()
	if str(sys.argv[1]) == "-u":
		data = [{"name": getname(str(sys.argv[2])),
				"link": str(sys.argv[2])
		}]
	else:
		data = getlist()
	enroll(data)

if __name__ == "__main__":
	main()