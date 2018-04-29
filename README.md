gggolfclient is a command-line interface for GGGolf.

___
## Usage

**Make a reservation for the first available time slot**
> gggolfclient.py res -d DAY -c COURSE... [-a HOUR -i]


**Find available time slots**
> gggolfclient.py find -d DAY -c COURSE... [-a HOUR -i]


**Make a quick reservation for a specific date and time**
> gggolfclient.py quick_res -D DATE -t TIME -c COURSE


**More usages**
> gggolfclient.py (-h | --help)

> gggolfclient.py (-v | --version)

___

### Commands:
>  res                 Reserve the first available time slot for wanted golf courses

>  quick_res           Reserve the specified time slot for wanted golf courses

>  find                Find Available Time slots for wanted golf courses

___

### Arguments:
>  DAY                 e.g. Monday

>  HOUR                e.g. 15

>  COURSE              W/B, W/R, R/9, B/9, G/B, 12 holes

>  TIME                e.g. 15:04

___

### Options:
>  -h --help           Show this screen.

>  -v --version        Show version.

>  -i --info           Show stacktrace.

>  -d --day=DAY        Specify a day of the week.

>  -t --time=TIME      Specify time of the day in 24h format.

>  -a --after=HOUR     Specify an hour in 24h format.

>  -c --course=COURSE  Specify the type of course.

>  -D --Date=DATE      Specify a date e.g. Apr 29.

