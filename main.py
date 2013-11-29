from getpass import *
from fb import *
from clev import *
import time

fb = FB(raw_input("email: "), getpass())
clev = Clev()


chats = []

def add_chat(name):
	c = FB.Chat(fb, name)
	c.open()
	chats.append(c)

who = None
while who != "":
	who = raw_input("who? ")
	if who != "":
		add_chat(who)

while 1 == 1:
	for chat in chats:
		if chat.has_new_message():
			clev.say(chat.get_message(), chat.send)
	time.sleep(1)