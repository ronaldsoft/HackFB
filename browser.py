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

	def __del__(self):
		# exit firefox driver upon deletion
		self.quit()