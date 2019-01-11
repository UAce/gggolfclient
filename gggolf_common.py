# gggolf_common.py: Common functions to work with gggolf
#!/usr/bin/env python
# 
# (C) Copyright 2018-2019 Yu-Yueh Liu

import credentials_info
import requests, sys, datetime, re, ast
from datetime import datetime, time
from collections import OrderedDict
from exception import *
from bs4 import BeautifulSoup


cookie_data = {}
referer = ""
s = requests.Session()
# list_of_days=OrderedDict([("Sunday", 0), ("Monday", 1), ("Tuesday", 2), ("Wednesday", 3), ("Thursday", 4), ("Friday", 5), ("Saturday", 6)])
list_of_days=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
list_of_courses=["W/B", "W/R", "R/9 (9)", "B/9 (9)", "G/B", "12 holes"]
list_of_months=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


##########################################
#                 QUERIES                #
##########################################

# HTTP GET request
def gggolf_get(func):
	global referer
	url =  credentials_info.base_url + func
	r = s.get(url,cookies = cookie_data, headers={'Referer': referer})
	referer = url
	return r

# HTTP POST request
def gggolf_post(func, req):
	global referer
	url = credentials_info.base_url + func
	res = s.post(url,data = req,cookies = cookie_data,headers = {'Referer': referer})
	referer = url
	return res

# gggolf Login Request
def gggolf_login():
	r=gggolf_get("index.php?option=com_ggmember&req=login&lang=en")
	token=get_token(r.text)
	# print "SECURITY TOKEN: "+token+"\n"
	res=gggolf_post("index.php?option=com_users&task=user.login&lang=en",{'username': credentials_info.username, 'password': credentials_info.password, 'option': 'com_users', 'task': 'user.login', 'return': 'aHR0cHM6Ly9zZWN1cmUuZ2dnb2xmLmNhL2NlcmYvaW5kZXgucGhwP29wdGlvbj1jb21fZ2dtZW1iZXImcmVxPWluZGV4Jmxhbmc9ZW4mbXNncz1Q', token : '1'})
	return res




##########################################
#             SEARCH & PARSE             #
##########################################


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
			date=daysOfMonth[counter].get_text().strip()
			urlValue=d.find("a")['href'].strip()
			listOfDates.append((date,urlValue))
		counter+=1

	# Return a dictionary with the Dates as keys in order of insertion (chronological order)
	# e.g. OrderedDict([(u'Apr 29', u'https://secure.gggolf.ca/cerf/index.php?option=com_ggmember&req=autogrid&lang=en&p0=Transaction&v0=FindTeeTimes&p1=Res&v1=D&p2=RequestDate&v2=20180429'), (u'May 06', u'https://secure.gggolf.ca/cerf/index.php?option=com_ggmember&req=autogrid&lang=en&p0=Transaction&v0=FindTeeTimes&p1=Res&v1=D&p2=RequestDate&v2=20180506')])
	return OrderedDict(listOfDates)

	
# Parse a Tee Time url and return url of first available slots for that Tee Time
def parse_tee_time(text, course_list, atime, date, nb_of_pl, show):
	html = BeautifulSoup(text,'html.parser')
	playerColNo=None
	courseColNo=None
	after_time=datetime.strptime(atime+":00", '%H:%M').time()
	# Remove Table headers and keep the table body
	tr_all=html.table.find_all("tr")[5:]
	# Get column number for Player 1 and for Course
	for th in html.table.select("tr.autogridHeader")[0].find_all("th"):
		if get_text(th)=="Player 1":
			playerColNo=int(th['data-colno'])
		if get_text(th)=="Course":
			courseColNo=int(th['data-colno'])
	first_time_slot_url=None
	isFirst=True
	if show:
		print "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		print "@   Available Tee Times for "+date+":   @"
		print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		print "Number of player: "+str(nb_of_pl)+"\n"

	for tr in tr_all:
		tr_list=tr.find_all("td")

		# Skip tee time if unavailable or not wanted course
		# is_valid_nb_of_player(nb_of_pl, tr_list)
		if not is_valid_nb_of_player(nb_of_pl, tr_list, playerColNo) or get_text(tr_list[courseColNo]) not in course_list:
			continue
		tmp=get_text(tr_list[1])
		tr_time=datetime.strptime(tmp, '%H:%M').time()
		isBookable=tr_list[0].find("a")
		if tr_time >= after_time and isBookable is not None:
			message=get_text(tr_list[2])+" course on "+date+" at "+tr_time.strftime("%H:%M")
			if show:
				print tr_time.__format__("%H:%M"), ":", get_text(tr_list[2])
				# print tr_list[0].find("a")['href'].strip()
			if isFirst:
				# Get the url of the first time slot
				first_time_slot_url=(message, get_url_action(tr_list[0].find("a")['href'].strip()))
				isFirst=False
	if first_time_slot_url is None:
		print "There are no available tee times for "+date+"..."
		print_short_line()
		return
		# raise NoResultException("No available time slot found for "+", ".join(course_list)+" courses...")
	else:
		if show:
			print_short_line()
		return first_time_slot_url


# Find the date with Tee Time for wanted day of the week
def search_tee_time_date_advance(text, date):
	text = text.replace('&nbsp;',' ') # hack to bypass how Python handles unicode
	html = BeautifulSoup(text,'html.parser')
	daysOfMonth = html.body.findAll("th", {"class" : "otherMonth"})
	daysContent = html.table.findAll("td", {"class" : "calendarDay"})
	counter=0
	for d in daysOfMonth:
		if d.text.find(date) > -1:
			urlValue=daysContent[counter].find("a")['href'].strip()
			# print urlValue
			return get_url_action(urlValue)
		counter+=1


def parse_tee_time_advance(text, course, time, date):
	html = BeautifulSoup(text,'html.parser')
	timeColNo=None
	courseColNo=None
	# Remove Table headers and keep the table body
	tr_all=html.table.find_all("tr")[5:]
	# Get column number for Player 1 and for Course
	for th in html.table.select("tr.autogridHeader")[0].find_all("th"):
		if get_text(th)=="Time":
			timeColNo=int(th['data-colno'])
		if get_text(th)=="Course":
			courseColNo=int(th['data-colno'])
	for tr in tr_all:
		tr_list=tr.find_all("td")

		# Skip tee time if unavailable or not wanted course
		if get_text(tr_list[timeColNo]) != time or get_text(tr_list[courseColNo]) != course:
			continue
		isBookable=tr_list[0].find("a")
		if isBookable:
			message=course+" course on "+date+" at "+time
			return (message, get_url_action(tr_list[0].find("a")['href'].strip()))
	# No result
	raise NoResultException("There are no "+course+" course available at "+time+"... Please try another date or time.")


##########################################
#                VALIDATION              #
##########################################


# Validate course, day, month
def is_valid(elem, thelist):
	# if not any(course in elem for elem in list_of_courses):
	if elem not in thelist:
		raise InvalidInput(elem+" is not valid!! Please Choose from the following:\n- "+ "\n- ".join(thelist))


# Validate reservation
def is_reservation_success(text):
	text = text.replace('&nbsp;',' ') # hack to bypass how Python handles unicode
	html = BeautifulSoup(text,'html.parser')
	if "Error in your request" in text:
		spans = html.body.findAll("span", {"class":"cR sB t2 aC"})
		message=""
		for span in spans:
			message+=get_text(span)+" "
		# print message
		raise Exception("Your reservation was not successful...\nError Message: "+message)
	else:
		print "\033[1;32m**** Congratulations, your reservation was successful!! ****\033[1m"
		sys.exit(0)


def is_valid_nb_of_player(nb, tr_list, player_column):
	result=True
	for i in range(3,3-nb,-1):
		result=result and (get_text(tr_list[player_column+i]) == "" or get_text(tr_list[player_column+i]) == "(9 holes only)")
	return result




##########################################
#                 GETTERS                #
##########################################


def get_user_id(text):
	text = text.replace('&nbsp;',' ') # hack to bypass how Python handles unicode
	html = BeautifulSoup(text,'html.parser')
	js_script=html.head.findAll("script", {"type" : "text/javascript"}, src=False)[0]
	fav=re.search(r'\"favorites\":\[s*([^].]+|\S+)', js_script.text).group(1).split("},")
	for f in fav:
		# print f.replace("}","")+"}"
		tmp=ast.literal_eval(f.replace("}","")+"}")
		if credentials_info.name in tmp['name']:
			return tmp['key']
	raise Exception("You are not a valid user... Please verify your name in credentials_info.py")


def get_token(text):
	text = text.replace('&nbsp;',' ') # hack to bypass how Python handles unicode
	soup = BeautifulSoup(text,'html.parser')
	token=""
	for n in soup.findAll('input'):
		if n['type']=="hidden" and n['value']=="1":
			token=n['name']
	return token


def get_arguments(docopt_args):
  course_list=remove_duplicate(docopt_args["--course"])
  reservation_day=docopt_args["--day"]
  nb_of_pl=int(docopt_args["--number"])
  after_time="8"

  # Check if the courses are valid
  for course in course_list:
	is_valid(course, list_of_courses)

  # Check if the after time is valid
  if docopt_args["--after"]:
    if int(docopt_args["--after"])<24 and int(docopt_args["--after"])>=0:
      after_time=docopt_args["--after"]
    else:
      raise InvalidInput('Invalid Time!')

  if nb_of_pl<=0 or nb_of_pl>4:
  	raise InvalidInput('You must be at least 1 player and at most 4 players!!!')

  message=reservation_day+" after "+after_time+"h for "+str(nb_of_pl)+" player(s)"

  # Check if reservation day is valid
  is_valid(reservation_day, list_of_days)
  
  return {"course_list":course_list, "reservation_day":reservation_day, "after_time":after_time, "player": nb_of_pl, "message":message}



def get_advance_arguments(docopt_args):
	# <pre>gggolfclient.py advance_res -M MONTH -D DATE -t TIME -c COURSE</pre>

	# Get arguments
	reservation_course=docopt_args["--course"][0]
	reservation_month=docopt_args["--Month"]
	reservation_date=docopt_args["--Date"]
	if int(reservation_date)<10 and len(reservation_date)==1:
		reservation_date="0"+reservation_date # e.g. 3 becomes 03
	reservation_time=docopt_args["--time"]
	
	# Validate arguments
	is_valid(reservation_course, list_of_courses)
	is_valid(reservation_month, list_of_months)
	datetime(datetime.now().year, int(list_of_months.index(reservation_month)+1), int(reservation_date)) # This validates the month and date
	reservation_time=datetime.strptime(reservation_time, '%H:%M').time() # This validates the time? at least for the format
	message=reservation_course+" course on "+reservation_month+" "+reservation_date+" at "+reservation_time.__format__("%H:%M")

	return {"course":reservation_course, "month":reservation_month, "date":reservation_date, "time":reservation_time.__format__("%H:%M"), "message":message}


def get_url_action(url):
	return url.replace("https://secure.gggolf.ca/cerf/", "")	


def get_text(elem):
	return elem.get_text().strip()



##########################################
#          OTHER USEFUL FUNCTIONS        #
##########################################


def remove_duplicate(alist):
	aset=set([elem for elem in alist if alist.count(elem) > 0])
	return list(aset)


def print_long_line():
	print "_____________________________________________________________________\n"


def print_short_line():
	print "\n_________________________________________________"