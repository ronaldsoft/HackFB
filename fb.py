from browser import *

class FB(Browser):

	# open a facebook window
	def __init__(self, email, password):
		Browser.__init__(self)
		self.__email = email
		self.__password = password
		self.get("http://www.facebook.com")
		self.login()

	
	# from login screen, login with given credentials
	def login(self):
		self.ensureURL('https://www.facebook.com/login')
		elem = self.find_element_by_id('email')
		self.fill(self.find_element_by_id('email'), self.__email)
		self.fill(self.find_element_by_id('pass'), self.__password, True)

	# submits logout form, returns to login menus
	def logout(self):
		self.find_element_by_id('logout_form').submit()

	# posts a status on own wall
	def postStatus(self, text):
		self.ensureURL('https://www.facebook.com')
		self.fill(self.find_element_by_id('u_0_1m'), text)
		self.find_element_by_id('u_0_1a').submit()

	class Chat:

		def __init__(self, name):
			self.__name = name
			self.__messages = []
			self.__newMessages = []

		def getMessages(self):
			self.__messages = self.__newMessages[:]
			self.__newMessages = []

