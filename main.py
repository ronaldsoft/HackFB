import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Browser(webdriver.Firefox):

	def __init__(self):
		webdriver.Firefox.__init__(self)

	def goTo(self, url):
		self.get(url)

	def byId(self, id):
		return self.find_element_by_id(id)

	def fill(self, elem, text, sub=False):
		elem.send_keys(text)
		if sub:
			elem.send_keys(Keys.RETURN)


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

	def logout(self):




# elem = driver.find_element_by_name("q")
# elem.send_keys("selenium")
# elem.send_keys(Keys.RETURN)
# assert "Google" in driver.title



fb = FB(raw_input("email: "), getpass.getpass())