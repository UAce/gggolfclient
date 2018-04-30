#!/usr/bin/env python
# The command-line interface for secure GGGolf
# (C) Copyright 2018-2019 Yu-Yueh Liu

"""Secure GG Golf Command-Line Interface

Usage:
  gggolfclient.py res -d DAY -c COURSE... -n NUMBER [-a HOUR -i]
  gggolfclient.py find -d DAY -c COURSE... -n NUMBER [-a HOUR -i]
  gggolfclient.py advance_res -M MONTH -D DATE -t TIME -c COURSE [-i]
  gggolfclient.py (-h | --help)
  gggolfclient.py (-v | --version)


Commands:
  res                 Reserve the first available time slot for wanted golf courses
  advance_res         Reserve the specified time slot for wanted golf courses
  find                Find Available Time slots for wanted golf courses


Arguments:
  DAY                 Day of the week e.g. Monday
  HOUR                Hour in 24h format e.g. 15
  COURSE              W/B, W/R, R/9 (9), B/9 (9), G/B, 12 holes
  TIME                Time in HH:MM format e.g. 15:04
  MONTH               First 3 letters of a month e.g. Apr
  DATE                Any number between 1 to 31 (depends on the month)
  NUMBER              Number of player


Options:
  -h --help           Show this screen.
  -v --version        Show version.
  -i --info           Show stacktrace.
  -d --day=DAY        Specify a day of the week.
  -t --time=TIME      Specify time of the day in 24h format.
  -a --after=HOUR     Specify an hour in 24h format.
  -c --course=COURSE  Specify the type of course.
  -M --Month=MONTH    Specify a month e.g. Apr.
  -D --Date=DATE      Specify a date e.g. 29.
  -n --number=NUMBER  Specify number of player (Max 4).

"""
from docopt import docopt
from gggolf_common import *
import credentials_info, sys

def main(docopt_args):
    print_long_line()

    # Hide Stacktrace if silent flag present
    sys.tracebacklimit=0
    if docopt_args["--info"]:
        sys.tracebacklimit=1

    if docopt_args["advance_res"]:
      message_and_reservation_url=exec_advance_find(get_advance_arguments(docopt_args))
      print "Reserving "+message_and_reservation_url[0]+"...\n"
      exec_reservation(message_and_reservation_url[1])


    # Reservation
    if docopt_args["res"]:
        message_and_reservation_urls=exec_find(get_arguments(docopt_args), 0)
        for elem in message_and_reservation_urls:
          print "\nReserving "+elem[0]+"\n"
          exec_reservation(elem[1])
          
    elif docopt_args["find"]:
        ulist=exec_find(get_arguments(docopt_args), 1)



def exec_find(args, show):
  show_available_times=None
  print "Finding available Tee Times",args["message"],"for the following courses:\n-","\n- ".join(args["course_list"]),"\n"

  main_html=gggolf_login()
  
  # e.g. OrderedDict([(u'Apr 29', u'https://secure.gggolf.ca/cerf/index.php?option=com_ggmember&req=autogrid&lang=en&p0=Transaction&v0=FindTeeTimes&p1=Res&v1=D&p2=RequestDate&v2=20180429'), (u'May 06', u'https://secure.gggolf.ca/cerf/index.php?option=com_ggmember&req=autogrid&lang=en&p0=Transaction&v0=FindTeeTimes&p1=Res&v1=D&p2=RequestDate&v2=20180506')])
  available_tee_times=search_tee_time_dates(main_html.text, list_of_days.index(args["reservation_day"]))
  reservation_urls=[]

  for date in available_tee_times:
    tee_time_url=get_url_action(available_tee_times[date])
    r=gggolf_get(tee_time_url)
    text = r.text.replace('&nbsp;',' ') # hack to bypass how Python handles unicode
    val=parse_tee_time(text, args["course_list"], args["after_time"], date, args["player"], show)
    # Don't append value if None
    if val:
      reservation_urls.append(val)

  # If list is empty, it means that there were no available time slots
  if len(reservation_urls) is 0:
    raise NoResultException("No availability for "+", ".join(course_list)+" courses... Please try with another golf course or another day of the week")
  else:
    return reservation_urls


def exec_reservation(url):
  r=gggolf_get(url)
  user_id=get_user_id(r.text)  
  res=gggolf_post(url, {'foursome0_player0_player': user_id, 'foursome0_player1_player': "guest", 'foursome0_player1_player': 'guest', 'foursome0_player3_player': 'guest', 'SaveTeeTime': 'Save'})
  is_reservation_success(res.text)


def exec_advance_find(args):
  # print "Finding "+args['message']+"...\n"

  main_html=gggolf_login()

  tee_time_url=search_tee_time_date_advance(main_html.text, args["month"]+" "+args["date"])
  r=gggolf_get(tee_time_url)
  text = r.text.replace('&nbsp;',' ') # hack to bypass how Python handles unicode

  return parse_tee_time_advance(text, args["course"], args["time"], args["month"]+" "+args["date"]) # e.g. ("message", "url")


# START OF SCRIPT
if __name__ == '__main__':
    args = docopt(__doc__, version='gggolfclient 1.0')
    # print(args)
    main(args)