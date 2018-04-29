#!/usr/bin/env python
# The command-line interface for secure GGGolf
# (C) Copyright 2018-2019 Yu-Yueh Liu

"""Secure GG Golf Command-Line Interface

Usage:
  gggolfclient.py res -d=DAY -c=COURSE... [-a=HOUR -s]
  gggolfclient.py test
  gggolfclient.py (-h | --help)
  gggolfclient.py (-v | --version)


Commands:
  res                 Reserve golf course
  test                Testing new function

Arguments:
  DAY
  HOUR
  COURSE              W/B, W/R, R/9, B/9, G/B, 12 holes

Options:
  -h --help           Show this screen.
  -v --version        Show version.
  -n --name=NAME      Golf Course location name.
  -d --day=DAY        Specify a day of the week.
  -a --after=HOUR     Specify an hour in 24h format
  -c --course=COURSE  Specify the type of course
  -s --silent

"""
from docopt import docopt
from gggolf_common import *
import credentials_info, sys

days={"Sunday":0, "Monday": 1, "Tuesday": 2, "Wednesday" : 3, "Thursday" : 4, "Friday": 5, "Saturday" : 6}


def main(docopt_args):
    
    # Hide Stacktrace if silent flag present
    if docopt_args["--silent"]:
        sys.tracebacklimit=0

    # Reservation
    if docopt_args["res"]:        
        course_list=docopt_args["--course"]
        # Get arguments
        after_time="8"
        if docopt_args["--after"]:
          if int(docopt_args["--after"])<24 and int(docopt_args["--after"])>0:
            after_time=docopt_args["--after"]
          else:
            raise Exception('Invalid Time!')

        
        reservation_day=docopt_args["--day"]
        if reservation_day not in days:
          print "This is not a valid day..."
        else:
          print "Reserving for "+reservation_day+" after "+after_time+"h ..."
          print "For courses:", course_list, "\n"
          # reserve_course(reservation_day)
          test_func(reservation_day, course_list, after_time)
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



def test_func(day, course_list, after):
  index=gggolf_login()
  url_list=search_tee_time(index.text, days[day])
  for url in url_list:
    search_available_slots(get_url_action(url), course_list, after)



# START OF SCRIPT
if __name__ == '__main__':
    args = docopt(__doc__, version='gggolfclient 1.0')
    # print(args)
    main(args)