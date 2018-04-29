#!/usr/bin/env python
# The command-line interface for secure GGGolf
# (C) Copyright 2018-2019 Yu-Yueh Liu

"""Secure GG Golf Command-Line Interface

Usage:
  gggolfclient.py res -d DAY -c COURSE... [-a=HOUR -i]
  gggolfclient.py find -d DAY -c COURSE... [-a=HOUR -i]
  gggolfclient.py quick_res -D DATE -t TIME -c COURSE
  gggolfclient.py (-h | --help)
  gggolfclient.py (-v | --version)


Commands:
  res                 Reserve the first available time slot for wanted golf courses
  quick_res           Reserve the specified time slot for wanted golf courses
  find                Find Available Time slots for wanted golf courses

Arguments:
  DAY                 e.g. Monday
  HOUR                e.g. 15
  COURSE              W/B, W/R, R/9, B/9, G/B, 12 holes
  TIME                e.g. 15:04

Options:
  -h --help           Show this screen.
  -v --version        Show version.
  -i --info           Show stacktrace.
  -d --day=DAY        Specify a day of the week.
  -t --time=TIME      Specify time of the day in 24h format.
  -a --after=HOUR     Specify an hour in 24h format.
  -c --course=COURSE  Specify the type of course.
  -D --Date=DATE      Specify a date e.g. Apr 29.

"""
from docopt import docopt
from gggolf_common import *
import credentials_info, sys

def main(docopt_args):
    print "_______________________________________________________________\n"

    # Hide Stacktrace if silent flag present
    sys.tracebacklimit=0
    if docopt_args["--info"]:
        sys.tracebacklimit=1

    if docopt_args["quick_res"]:
      print "Quick Reservation for..."
      exec_quick_reservation(get_quick_argument(docopt_args))

    # Reservation
    if docopt_args["res"]:
        reservation_urls=exec_find(get_argument(docopt_args), 0)
        for elem in reservation_urls:
          print "\nReserving "+elem[0]+"\n"
          # print get_url_action(elem[1])
          exec_reservation(get_url_action(elem[1]))
    elif docopt_args["find"]:
        exec_find(get_argument(docopt_args), 1)

        # elif docopt_args["--greatflag"]:
        #     print "   with --greatflag\n"
        # else:
        #     print "Not a valid command"
    # elif docopt_args["test"]:
    #     test_func()
    # For 1 or more repeating arguments with ./gggolfclient <repeating>...
    # elif docopt_args["<repeating>"]:
    #     print "You have used the repeating args:"
    #     print '   ' + '   '.join(docopt_args["<repeating>"]) + ' '


def exec_find(args, show):
  show_available_times=None
  print "Finding available slots",args["message"],"for the following courses:\n-","\n- ".join(args["course_list"])

  main_html=gggolf_login()
  
  # e.g. OrderedDict([(u'Apr 29', u'https://secure.gggolf.ca/cerf/index.php?option=com_ggmember&req=autogrid&lang=en&p0=Transaction&v0=FindTeeTimes&p1=Res&v1=D&p2=RequestDate&v2=20180429'), (u'May 06', u'https://secure.gggolf.ca/cerf/index.php?option=com_ggmember&req=autogrid&lang=en&p0=Transaction&v0=FindTeeTimes&p1=Res&v1=D&p2=RequestDate&v2=20180506')])
  available_tee_times=search_tee_time_dates(main_html.text, list_of_days[args["reservation_day"]])
  reservation_urls=[]

  for date in available_tee_times:
    tee_time_url=get_url_action(available_tee_times[date])
    reservation_urls.append(parse_tee_time(tee_time_url, args["course_list"], args["after_time"], date, show))
  return reservation_urls


def exec_reservation(url):
  r=gggolf_get(url)
  # print r.text
  user_id=get_user_id(r.text)  
  res=gggolf_post(url, {'foursome0_player0_player': user_id, 'foursome0_player1_player': "guest", 'foursome0_player1_player': 'guest', 'foursome0_player3_player': 'guest', 'SaveTeeTime': 'Save'})
  is_reservation_success(res.text)


def exec_quick_reservation(url):
  pass


# START OF SCRIPT
if __name__ == '__main__':
    args = docopt(__doc__, version='gggolfclient 1.0')
    # print(args)
    main(args)