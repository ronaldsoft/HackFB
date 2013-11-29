from browser import *
from threading import Timer
import time


########################################
#####           Facebook           #####
# ======================================
# - encompasses a Facebook firefox window
# - 
# 
class FB(Browser):

	# open a facebook window
	def __init__(self, email, password):
		Browser.__init__(self)
		self.__email = email
		self.__password = password
		self.get("http://www.facebook.com")
		self.login()
		self.toggle_chat_list()

	
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
	def post_status(self, text):
		elem = self.find_element_by_css_selector('textarea')
		elem.click()
		elem.clear()
		self.find_element_by_css_selector("li > button").click()
		elem = self.find_element_by_css_selector('textarea')
		self.fill(elem, text)
		# self.find_element_by_css_selector("li > button").click()

	# opens and closes the list viewer
	def toggle_chat_list(self):
		self.runJS("document.getElementsByClassName('fbNubButton')[1].click()")

	def close_chats(self):
		self.execute_script(""" buttons = document.getElementsByClassName('close button');
								for(var i = 0; i < buttons.length; i++){
									buttons[i].click()
								}""")

	# access icons at page header
	def count_notifications(self):
		return int(self.find_element_by_id('notificationsCountValue').get_attribute('innerHTML'))
	def count_messages(self):
		return int(self.find_element_by_id('mercurymessagesCountValue').get_attribute('innerHTML'))
	def count_friend_requests(self):
		return int(self.find_element_by_id('requestsCountValue').get_attribute('innerHTML'))

	# clicks the 'Home' button at top of fb window
	def go_home(self):
		self.find_element_by_css_selector('#navHome > a').click()

	# goes to the currently logged in user's profile
	def view_own_profile(self):
		self.find_element_by_css_selector('#navTimeline > a').click()

	# automatically accepts first result of search
	def graph_search(self, what):
		bar = self.find_element_by_class_name('_586i')
		bar.click()
		bar.clear()
		bar.send_keys(what)
		bar.send_keys(Keys.RETURN)

	


	####################################
	#####           Chat           #####
	# ==================================
	# - encompasses a Facebook chat tab
	# - should not be interfered with by user (it doesn't detect events)
	# 
	class Chat:

		# initiates a chat with a specific person
		# - 'parent' should by parent fb window
		def __init__(self, parent, name, clear=True):
			self.__par = parent
			self.__name = name
			self.__message = ""
			self.__prevMessage = ""
			self.__linked = False
			self.__linkedWith = None

		# ensures that chat tab is open
		# - currently does not work for offline users
		def open(self):
			self.__par.execute_script(""" people = document.getElementsByClassName('_52zl');
										    for(var i = 0; i < people.length; i++){
										    	if(people[i].innerHTML.toUpperCase() == '""" + self.__name + """'.toUpperCase()){
										    		people[i].click(); break;
										    	}
										    }""")

		def close(self):
			self.open()
			self.__par.execute_script(""" chats = document.getElementsByClassName('fbNubFlyout fbDockChatTabFlyout');
											for(var i = 0; i < chats.length; i++){
												if(chats[i].getElementsByClassName('titlebarText')[0].innerHTML.toUpperCase() == '""" + self.__name + """'.toUpperCase()){
													var chat = chats[i];
													var closeButton = chat.getElementsByClassName('close button')[0];
													closeButton.click();
													break;
												}
											}""")

		def send(self, text):
			self.open()
			self.__par.execute_script(""" chats = document.getElementsByClassName('fbNubFlyout fbDockChatTabFlyout');
											for(var i = 0; i < chats.length; i++){
												if(chats[i].getElementsByClassName('titlebarText')[0].innerHTML.toUpperCase() == '""" + self.__name + """'.toUpperCase()){
													var chat = chats[i];
													var msgBox = chat.getElementsByClassName('uiTextareaAutogrow _552m')[0];
													msgBox.value = '""" + text + """';
													var e = new Event("keydown");
													e.keyCode = 13;
													msgBox.dispatchEvent(e);
													break;
												}
											}""")
			self.get_message()

		# grabs the most recent message in chat tab
		def get_message(self, getAll=False):
			self.open()
			self.__prevMessage = self.__message
			self.__message = str(self.__par.execute_script(""" chats = document.getElementsByClassName('fbNubFlyout fbDockChatTabFlyout');
								for(var i = 0; i < chats.length; i++){
									if(chats[i].getElementsByClassName('titlebarText')[0].innerHTML.toUpperCase() == '""" + self.__name + """'.toUpperCase()){
										var chat = chats[i];
										var divs = chat.querySelectorAll('[data-jsid~=message]>span');
										return divs[divs.length-1].getElementsByTagName('span')[0].innerHTML;
										break;
									}
								}"""))
			return self.__message

		# Returns true if a new message has been recieved since the last call
		# of 'get_message()'.
		def has_new_message(self):
			return self.__message != self.__prevMessage

		# Marks most recent message as read. has_new_message will no longer return True
		def mark_as_read(self):
			self.__prevMessage = self.__message

		# Getter method (names of chat objects should not be changed).
		def get_name(self):
			return self.__name

