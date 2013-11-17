from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains as do



class Browser(webdriver.Firefox):

	def __init__(self):
		webdriver.Firefox.__init__(self)

	def ensureURL(self, expected):
		if self.current_url == expected:
			self.get(expected)

	def fill(self, elem, text, sub=False):
		elem.send_keys(text)
		if sub:
			elem.send_keys(Keys.RETURN)

	def __del__(self):
		a = 1
		# self.quit()