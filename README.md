gggolfclient is a command-line interface for GGGolf.

___
## Usage

**Make a reservation for the first available time slot**
<pre>gggolfclient.py res -d DAY -c COURSE... [-a HOUR -i]</pre>


**Find available time slots**
<pre>gggolfclient.py find -d DAY -c COURSE... [-a HOUR -i]</pre>


**Make a quick reservation for a specific date and time**
<pre>gggolfclient.py quick_res -D DATE -t TIME -c COURSE</pre>


**More usages**
<pre>
gggolfclient.py (-h | --help)
gggolfclient.py (-v | --version)
</pre>
___

### Commands:
<pre>
res                 Reserve the first available time slot for wanted golf courses
quick_res           Reserve the specified time slot for wanted golf courses
find                Find Available Time slots for wanted golf courses
</pre>

___

### Arguments:
<pre>
DAY                 e.g. Monday

HOUR                e.g. 15

COURSE              W/B, W/R, R/9 (9), B/9 (9), G/B, 12 holes

TIME                e.g. 15:04
</pre>

___

### Options:
<pre>
-h --help           	Show this screen.

-v --version       		Show version.

-i --info           	Show stacktrace.

-d --day=DAY        	Specify a day of the week.

-t --time=TIME      	Specify time of the day in 24h format.

-a --after=HOUR     	Specify an hour in 24h format.

-c --course=COURSE  	Specify the type of course.

-D --Date=DATE      	Specify a date e.g. Apr 29.
</pre>

