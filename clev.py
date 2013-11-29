from browser import *
from threading import Timer
import time


########################################
#####           Facebook           #####
# ======================================
# - encompasses a Facebook firefox window
# - 
# 
class Clev(Browser):

	last = ""
	curr = ""

	# open a facebook window
	def __init__(self):
		Browser.__init__(self)
		self.get("http://www.cleverbot.com")

	def say(self, text, func=None):
		elem = self.find_element_by_id('stimulus')
		elem.click()
		elem.clear()
		self.fill(elem, text, True)
		last = text
		curr = text
		if func == None:
			return
		prev = ""
		curr = "not blank"
		while prev != curr or curr.find("<span") != -1:
			time.sleep(1)
			prev = curr
			curr = self.execute_script("return document.querySelector('span > span').innerHTML;")
		func(curr)

