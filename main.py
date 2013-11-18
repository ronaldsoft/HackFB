from getpass import *
from fb import *


fb = FB(raw_input("email: "), getpass())
 

# fb.implicitly_wait(10)
# print fb.getChatMessages()
# fb.logout()