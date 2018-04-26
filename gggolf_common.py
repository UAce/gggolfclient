# gggolf_common.py: Common functions to work with gggolf
#!/usr/bin/env python
# 
# (C) Copyright 2018-2019 Yu-Yueh Liu

import credentials_info
import requests,sys
import datetime
from datetime import datetime as dt
from bs4 import BeautifulSoup

cookie_data = {}
referer = ""
s = requests.Session()

def gggolf_get(func):
	# if verbose:
	# 	sys.stderr.write("? " + func + "\n")

	global referer
	url =  credentials_info.base_url + func
	r = s.get(url,cookies = cookie_data, headers={'Referer': referer})
	referer = url
	return r

def gggolf_post(func, req):
	# if verbose:
	# 	sys.stderr.write("> " + func + "\n")

	global referer
	url = credentials_info.base_url + func
	r = s.post(url,data = req,cookies = cookie_data,headers = {'Referer': referer})
	referer = url
	return r

def gggolf_login():
	r=gggolf_get("option=com_ggmember&req=login&lang=en")
	token=get_token(r.text)
	print "THE TOKEN is: "+token
	print "\n\n_________________________________________________________\n\n"
	
	r2=gggolf_post("option=com_users&task=user.login&lang=en",{'username': credentials_info.username, 'password': credentials_info.password, 'option': 'com_users', 'task': 'user.login', 'return': 'aHR0cHM6Ly9zZWN1cmUuZ2dnb2xmLmNhL2NlcmYvaW5kZXgucGhwP29wdGlvbj1jb21fZ2dtZW1iZXImcmVxPWluZGV4Jmxhbmc9ZW4mbXNncz1Q', token : '1'})
	return r2

def get_token(text):
	text = text.replace('&nbsp;',' ') # hack to bypass how Python handles unicode
	soup = BeautifulSoup(text,'html.parser')
	token=""
	for n in soup.findAll('input'):
		if n['type']=="hidden" and n['value']=="1":
			token=n['name']
	return token

def tee_times_parse(text):
	text = text.replace('&nbsp;',' ') # hack to bypass how Python handles unicode
	html = BeautifulSoup(text,'html.parser')
	table = html.body.find('table')
	# print table
	# print table
	for t in table:
		print t
		print "\n\n @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ \n\n"
	# tr = table.findAll('tr')[2:]
	# records = {}
	# for row in tr:
	# 	cells = row.findAll('td')
	# 	record = parse_entry(cells)

	# 	if record is None:
	# 		continue
	# 	elif record['subject'] is None: #This is notes, or additional days. I don't care about it right now
	# 		continue
			
	# 	record['_code'] = record['subject'] + "-" + record['course'] + "-" + record['section']

	# 	determine_state(record)

	# 	records[record['_code']] = record
	
	# print table

