from getpass import *
from fb import *


fb = FB(raw_input("email: "), getpass())
fb.getChatMessages()
fb.logout()