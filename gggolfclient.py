#!/usr/bin/env python
# The command-line interface for secure GGGolf
# (C) Copyright 2018-2019 Yu-Yueh Liu

"""Secure GG Golf Command-Line Interface

Usage:
  gggolfclient.py res -d DAY
  gggolfclient.py test
  gggolfclient.py (-h | --help)
  gggolfclient.py (-v | --version)


Commands:
  res             Reserve golf course
  test            Testing new function

Options:
  -h --help       Show this screen.
  -v --version    Show version.
  -n --name=NAME  Golf Course location name.
  -d --day=DAY    Day of the week.

"""
from docopt import docopt
from gggolf_common import *
import credentials_info

days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

def main(docopt_args):
    
    # # set variables
    # if docopt_args["setup"]:
    #   location_name=docopt_args["--name"]

    #   if location_name not in locations :
    #     print "This is not a valid location..."
    #   else:
    #     init("https://secure.gggolf.ca/"+location_name+"/index.php?")
    #     print "The setup is DONE! The location you have selected is: "+location_name
    #     print base_url+"\n"

    # Reservation
    if docopt_args["res"]:        
        res_day=docopt_args["--day"]
        # Get arguments
        if res_day not in days:
          print "This is not a valid day..."
        else:
          print "You have chosen to reserve on "+res_day
          reserve_course(res_day)
        # elif docopt_args["--greatflag"]:
        #     print "   with --greatflag\n"
        # else:
        #     print "Not a valid command"
    elif docopt_args["test"]:
        test_func()
    # For 1 or more repeating arguments with ./gggolfclient <repeating>...
    # elif docopt_args["<repeating>"]:
    #     print "You have used the repeating args:"
    #     print '   ' + '   '.join(docopt_args["<repeating>"]) + ' '


def reserve_course(day):
  gggolf_login()



def test_func():
  index=gggolf_login()
  tee_times_parse(index.text)



# START OF SCRIPT
if __name__ == '__main__':
    args = docopt(__doc__, version='gggolfclient 1.0')
    # print(args)
    main(args)