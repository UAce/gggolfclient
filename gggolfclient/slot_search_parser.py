import urllib2, credentials_info
from gggolf_common import *
from bs4 import BeautifulSoup


def parse(text):
	print("parse some stuff")
	print(text)
	# url = raw_input('Web-Address: ')

	# html = urllib2.urlopen('http://' +url).read()
	# soup = BeautifulSoup(html)
	# soup.prettify()
	# for anchor in soup.findAll('a', href=True):
	#     print(anchor['href'])