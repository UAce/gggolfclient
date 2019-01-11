gggolfclient is a command-line interface for GGGolf.

___
## Usage

**Make a reservation for the first available time slot for specified day of the week, number of people and course**
<pre>gggolfclient.py res -d DAY -c COURSE... -n NUMBER [-a HOUR -i]</pre>


**Find and display available time slots for specified day of the week, number of people and course**
<pre>gggolfclient.py find -d DAY -c COURSE... -n NUMBER [-a HOUR -i]</pre>


**Make an advanced reservation for a specific date, time and course**
<pre>gggolfclient.py advance_res -M MONTH -D DATE -t TIME -c COURSE [-i]</pre>


**Configure GGGolf credentials and location name**
<pre>gggolfclient.py configure</pre>

**More usages**
<pre>
gggolfclient.py (-h | --help)
gggolfclient.py (-v | --version)
</pre>
___

### Commands:
<pre>
res                 Reserve the first available time slot for wanted golf courses
advance_res         Reserve the specified time slot for wanted golf courses
find                Find Available Time slots for wanted golf courses
configure           Configure credentials and location name
</pre>

___

### Arguments:
<pre>
DAY                 Day of the week e.g. Monday

HOUR                Hour in 24h format e.g. 15

COURSE              W/B, W/R, R/9 (9), B/9 (9), G/B, 12 holes

TIME                Time in HH:MM format e.g. 15:04

MONTH               First 3 letters of a month e.g. Apr

DATE                Any number between 1 to 31 (depends on the month)

NUMBER              Number of people
</pre>

___

### Options:
<pre>
-h --help           	Show this screen.

-v --version        	Show version.

-i --info           	Show stacktrace.

-d --day=DAY        	Specify a day of the week.

-t --time=TIME      	Specify time of the day in 24h format.

-a --after=HOUR     	Specify an hour in 24h format.

-c --course=COURSE  	Specify the type of course.

-D --Date=DATE      	Specify a date e.g. Apr 29.

-n --number=NUMBER  	Specify number of people (Max 4 ppl).
</pre>

