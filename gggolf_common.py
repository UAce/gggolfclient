# gggolf_common.py: Common functions to work with gggolf
#!/usr/bin/env python
# 
# (C) Copyright 2018-2019 Yu-Yueh Liu

import credentials_info
import requests,sys
import datetime
from datetime import datetime, time
from collections import OrderedDict
from bs4 import BeautifulSoup

cookie_data = {}
referer = ""
s = requests.Session()

def gggolf_get(func):
	global referer
	url =  credentials_info.base_url + func
	r = s.get(url,cookies = cookie_data, headers={'Referer': referer})
	referer = url
	return r

def gggolf_post(func, req):
	global referer
	url = credentials_info.base_url + func
	r = s.post(url,data = req,cookies = cookie_data,headers = {'Referer': referer})
	referer = url
	return r

def gggolf_login():
	r=gggolf_get("index.php?option=com_ggmember&req=login&lang=en")
	token=get_token(r.text)
	print "SECURITY TOKEN: "+token+"\n"
	
	r2=gggolf_post("index.php?option=com_users&task=user.login&lang=en",{'username': credentials_info.username, 'password': credentials_info.password, 'option': 'com_users', 'task': 'user.login', 'return': 'aHR0cHM6Ly9zZWN1cmUuZ2dnb2xmLmNhL2NlcmYvaW5kZXgucGhwP29wdGlvbj1jb21fZ2dtZW1iZXImcmVxPWluZGV4Jmxhbmc9ZW4mbXNncz1Q', token : '1'})
	return r2

# Parse a Tee Time url and return all available time slots for that Tee Time
def parse_tee_time(tee_time_url, course_list, atime, show):
	r=gggolf_get(tee_time_url)
	text = r.text.replace('&nbsp;',' ') # hack to bypass how Python handles unicode
	html = BeautifulSoup(text,'html.parser')

	# Remove Table headers and keep the table body
	tr_all=html.table.find_all("tr")[5:]
	
	playerColNo=None
	courseColNo=None
	after_time=datetime.strptime(atime+":00", '%H:%M').time()

	# Get column number for Player 1 and for Course
	for th in html.table.select("tr.autogridHeader")[0].find_all("th"):
		if get_text(th)=="Player 1":
			playerColNo=int(th['data-colno'])
		if get_text(th)=="Course":
			courseColNo=int(th['data-colno'])

	available_time_urls=[]
	for tr in tr_all:
		# print tr
		tr_list=tr.find_all("td")

		# Skip tee time if unavailable or not wanted course
		if get_text(tr_list[playerColNo]) == "Unavailable" or get_text(tr_list[playerColNo]) != "" or get_text(tr_list[courseColNo]) not in course_list:	
			continue
		
		tmp=get_text(tr_list[1])
		tr_time=datetime.strptime(tmp, '%H:%M').time()
		isBookable=tr_list[0].find("a")
		if tr_time >= after_time and isBookable is not None:
			if show:
				print tr_time, ":", get_text(tr_list[2]), "is available" 
			available_time_urls.append(tr_list[0].find("a")['href'].strip())
	if len(available_time_urls) is 0:
		raise Exception("There are no available courses...")
	else:
		return available_time_urls


def get_url_action(url):
	return url.replace("https://secure.gggolf.ca/cerf/", "")	


def get_token(text):
	text = text.replace('&nbsp;',' ') # hack to bypass how Python handles unicode
	soup = BeautifulSoup(text,'html.parser')
	token=""
	for n in soup.findAll('input'):
		if n['type']=="hidden" and n['value']=="1":
			token=n['name']
	return token

# Find the dates with Tee Time for wanted day of the week
def search_tee_time_dates(text, day):
	text = text.replace('&nbsp;',' ') # hack to bypass how Python handles unicode
	html = BeautifulSoup(text,'html.parser')
	daysOfMonth = html.body.findAll("th", {"class" : "otherMonth"})
	daysContent = html.table.findAll("td", {"class" : "calendarDay"})
	# print "This is the index that we want:", day
	listOfDates=[]
	counter=0
	for d in daysContent:
		if d.text.find("Tee Times") > -1 and (counter%7) is day:
			date=daysOfMonth[counter].get_text().strip(	)
			urlValue=d.find("a")['href'].strip()
			listOfDates.append((date,urlValue))
		counter+=1

	# Return a dictionary with the Dates as keys in order of insertion (chronological order)
	# e.g. OrderedDict([(u'Apr 29', u'https://secure.gggolf.ca/cerf/index.php?option=com_ggmember&req=autogrid&lang=en&p0=Transaction&v0=FindTeeTimes&p1=Res&v1=D&p2=RequestDate&v2=20180429'), (u'May 06', u'https://secure.gggolf.ca/cerf/index.php?option=com_ggmember&req=autogrid&lang=en&p0=Transaction&v0=FindTeeTimes&p1=Res&v1=D&p2=RequestDate&v2=20180506')])
	return OrderedDict(listOfDates)

def get_text(elem):
	return elem.get_text().strip()