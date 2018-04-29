#!/usr/bin/env python
# The command-line interface for secure GGGolf
# (C) Copyright 2018-2019 Yu-Yueh Liu

"""Secure GG Golf Command-Line Interface

Usage:
  gggolfclient.py <command> -d=DAY -c=COURSE... [-a=HOUR -s]
  gggolfclient.py (-h | --help)
  gggolfclient.py (-v | --version)


Commands:
  res                 Reserve the first available time slot for wanted golf courses
  find                Find Available Time slots for wanted golf courses

Arguments:
  DAY                 e.g. Monday
  HOUR                e.g. 15
  COURSE              W/B, W/R, R/9, B/9, G/B, 12 holes

Options:
  -h --help           Show this screen.
  -v --version        Show version.
  -d --day=DAY        Specify a day of the week.
  -a --after=HOUR     Specify an hour in 24h format
  -c --course=COURSE  Specify the type of course
  -s --silent         Hides stacktrace

"""
from docopt import docopt
from gggolf_common import *
import credentials_info, sys

list_of_days=OrderedDict([("Sunday", 0), ("Monday", 1), ("Tuesday", 2), ("Wednesday", 3), ("Thursday", 4), ("Friday", 5), ("Saturday", 6)])


def main(docopt_args):
    # Get command
    command=docopt_args["<command>"]
    after_time="8"

    # Hide Stacktrace if silent flag present
    if docopt_args["--silent"]:
        sys.tracebacklimit=0

    # Reservation
    if command:
        course_list=docopt_args["--course"]
        
        if docopt_args["--after"]:
          if int(docopt_args["--after"])<24 and int(docopt_args["--after"])>0:
            after_time=docopt_args["--after"]
          else:
            raise Exception('Invalid Time!')

        reservation_day=docopt_args["--day"]
        message=reservation_day+" after "+after_time+"h..."
        if reservation_day not in list_of_days:
          raise Exception('Invalid Day!! Please Choose one of the following days:\n- '+ "\n- ".join(list_of_days))
        elif command == "res":
          print "Reserving the first available slot for "+message
          print "The golf courses you chose:", course_list, "\n"
          search_available_times(reservation_day, course_list, after_time, 0)
        elif command == "find":
          print "Finding available slots for "+message
          print "The golf courses you chose:", course_list, "\n"
          search_available_times(reservation_day, course_list, after_time, 1)
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


def reserve_course(day):
  gggolf_login()



def search_available_times(day, course_list, after, show_available_times):
  main_html=gggolf_login()
  
  # e.g. OrderedDict([(u'Apr 29', u'https://secure.gggolf.ca/cerf/index.php?option=com_ggmember&req=autogrid&lang=en&p0=Transaction&v0=FindTeeTimes&p1=Res&v1=D&p2=RequestDate&v2=20180429'), (u'May 06', u'https://secure.gggolf.ca/cerf/index.php?option=com_ggmember&req=autogrid&lang=en&p0=Transaction&v0=FindTeeTimes&p1=Res&v1=D&p2=RequestDate&v2=20180506')])
  available_tee_times=search_tee_time_dates(main_html.text, list_of_days[day])
  # print available_tee_times
  for date in available_tee_times:
    if show_available_times: 
      print "Available Tee Times for "+date+": "
    tee_time_url=get_url_action(available_tee_times[date])
    available_url=parse_tee_time(tee_time_url, course_list, after, show_available_times)
    print "\n\n"
    for url in available_url:
      print url
    print "\n___________________________________________________\n"



# START OF SCRIPT
if __name__ == '__main__':
    args = docopt(__doc__, version='gggolfclient 1.0')
    # print(args)
    main(args)