#!/usr/bin/env python3

import logging
from datetime import datetime
from getpass import getpass
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
	global LOG
	LOG = "log.out"
	logging.basicConfig(filename=LOG, level=logging.DEBUG)
	global file_s, file_c
	file_s = 0
	file_c = 0

def login():
	#reads login info from json
	login = dict()
	try:
		with open("login.json") as f:
			login = json.load(f)	
	except:#todo - add login failure handling
		login["user"] = input("Email (gabriel.preite@studio.unibo.it): ")
		if login["user"] == "":
			login["user"] = "gabriel.preite@studio.unibo.it"
		login["password"] = getpass("Password: ")

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
	#gets course name from link
	page = s.get(link)
	soup = BeautifulSoup(page.content, "html.parser")
	name = re.search("<h1>(.+)</h1>", str(soup)).group()[4:-5]
	return name

def getres(link):
	#scans course for resources
	page = s.get(link)
	soup = BeautifulSoup(page.content, "html.parser")

	#finds all matches for the resource link type
	res_list = soup.find_all("a", {"class": "aalink", "href": re.compile("(.+)resource(.+)")})
	for res in res_list:
		res_page = s.get(res.get("href"))
		res_url = res_page.url
		logging.debug(datetime.now().strftime("%m/%d/%Y, %H:%M:%S\n")+res_url)

		#saves size in http header
		res = s.head(res_url)
		global file_s, file_c
		file_s += int(res.headers["Content-Length"])/1024
		file_c += 1

def enroll(data):
	counter = 0
	global file_s, file_c
	for item in data:
		counter += 1
		try:
			#scrape page
			page = s.get(item["link"])
			soup = BeautifulSoup(page.content, "html.parser")
			if re.search("(.+)Opzioni di iscrizione(.+)", str(soup)) == None:
				getres(item["link"])
				global file_s, file_c
				print("Logged "+str(file_s)+"kb in "+str(file_c)+" files")
				print("Scanned "+str(counter)+"/"+str(len(data))+" courses")
				continue

			#scrape fields from js generated code
			r_id = soup.find("input", {"name": "id"}).get("value")
			r_in = soup.find("input", {"name": "instance"}).get("value")
			r_sk = soup.find("input", {"name": "sesskey"}).get("value")
			r_qf_k = re.search("_qf__(.+)form", str(soup)).group()
			r_qf_v = soup.find("input", {"name": r_qf_k}).get("value")
			r_mf = soup.find("input", {"name": "mform_isexpanded_id_selfheader"}).get("value")

			#create post payload
			payload = {
				"id": r_id,
				"instance": r_in,
				"sesskey": r_sk,
				r_qf_k: r_qf_v,
				"mform_isexpanded_id_selfheader": r_mf
			}

			#send post to enroll
			s.post(CONFIG["url_enroll"], data=payload)
			p = s.get(item["link"])
			soup = BeautifulSoup(p.content, "html.parser")
			#todo - improve enrollment response detection
			if re.search("(.+)Opzioni di iscrizione(.+)", str(soup)) == None:
				#print("Enrolled in: "+item["name"])
				logging.debug(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+"\nEnrolled in: "+item["name"])
			else:
				#print("Closed course: "+item["name"])
				logging.debug(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+"\nClosed course: "+item["name"])
		except:
			#courses already enrolled in have no "enroll" button
			#print("Already enrolled in: "+item["name"])
			logging.debug(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+"\nAlready enrolled in: "+item["name"])
		getres(item["link"])
		print("Logged "+str(file_s)+"kb in "+str(file_c)+" files")
		print("Scanned "+str(counter)+"/"+str(len(data))+" courses")

def main():
	init()
	login()

	#cli argument logic
	if len(sys.argv) > 1 and str(sys.argv[1]) == "-u":
		data = [{"name": getname(str(sys.argv[2])),
			"link": str(sys.argv[2])
		}]
	else:
		data = getlist()

	enroll(data)

if __name__ == "__main__":
	main()