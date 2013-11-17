from browser import *

class FB(Browser):

	# open a facebook window
	def __init__(self, email, password):
		Browser.__init__(self)
		self.__email = email
		self.__password = password
		self.goTo("http://www.facebook.com")
		self.login()
	

	def login(self):
		# assuming login page, types email & password, then submits form
		self.fill(self.byId('email'), self.__email)
		self.fill(self.byId('pass'), self.__password, True)