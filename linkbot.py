#!python

import praw
import re
import ConfigParser
import time
from pprint import pprint
from time import time, sleep

user_agent = "link checker bot v1.2.0 by /u/shamwho"
config = ConfigParser.ConfigParser()
config.read("./linkbot.cfg")
last_time = time()

def validate(link):
	m = re.match('[ur]/[\W]*', body)
	if m:
		body_parts = body.split("/")
		if body_parts[0] == 'r':
			gen = r.get_subreddit(body_parts[1]).get_top(limit=1)
			try:
				sum(1 for _ in gen)
			except:
				return [False, 'r']
			else:
				return [True, 'r']
		else:
			try:
				gen = r.get_redditor(body_parts[1]).get_overview()
			except:
				return [False, 'u']
			else:
				return [True, 'u']
	return None

if __name__ == '__main__':
	r = praw.Reddit(user_agent=user_agent)
	r.login(config.get("account info","username"),config.get("account info","password"))
	user = r.get_redditor('LinkFixerBot')
	while True:
		gen = user.get_comments(sort='new',limit=10)
		first_checked = None
		for thing in gen:
			#print thing.created_utc
			if first_checked == None:
				first_checked = thing.created_utc
			if thing.created_utc <= last_time:
				last_time = first_checked
				break
			body = thing.body.strip().lstrip('/')
			result = validate(body)
			if result and result[0] == False:
				reply = ""
				if result[1] == 'r':
					reply += "Subreddit "
				else:
					reply += "User "
				reply += "doesn't exist"
				print body + ": " + reply
				thing.reply(reply)
				sleep(60)
		sleep(60)
