from browser import *

class FB(Browser):

	# open a facebook window
	def __init__(self, email, password):
		Browser.__init__(self)
		self.__email = email
		self.__password = password
		self.get("http://www.facebook.com")
		self.login()
		self.toggleChatList()

	
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
		elem = self.find_element_by_css_selector('textarea')
		elem.click()
		self.fill(elem, text)
		self.find_element_by_css_selector("li > button").click()

	# opens and closes the list viewer
	def toggleChatList(self):
		self.runJS("document.getElementsByClassName('fbNubButton')[1].click()")

	def closeChats(self):
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
	def view_profile(self):
		self.find_element_by_css_selector('#navTimeline > a').click()
		

	class Chat:

		# initiates a chat with a specific person
		# - 'parent' should by parent fb window
		def __init__(self, parent, name, clear=True):
			self.__par = parent
			self.__name = name
			self.__message = ""
			self.__prevMessage = ""
			# self.__gatherMessages()
			# if clear:
			# 	self.markAllAsUnread()


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
			self.getMessage()

		# grabs the most recent message in chat tab
		def getMessage(self, getAll=False):
			self.open()
			self.__prevMessage = self.__message
			self.__message = str(self.__par.execute_script(""" chats = document.getElementsByClassName('fbNubFlyout fbDockChatTabFlyout');
								for(var i = 0; i < chats.length; i++){
									if(chats[i].getElementsByClassName('titlebarText')[0].innerHTML.toUpperCase() == '""" + self.__name + """'.toUpperCase()){
										var chat = chats[i];
										var divs = chat.querySelectorAll('[data-jsid~=message]>span');
										return divs[divs.length-1].innerHTML;
										break;
									}
								}"""))
			return self.__message

		# Returns true if a new message has been recieved since the last call
		# of 'getMessage()'.
		def hasNewMessage(self):
			return self.__message != self.__prevMessage

		# Marks most recent message as read. hasNewMessage will no longer return True
		def markAsRead(self):
			self.__prevMessage = self.__message

		# Getter method (names of chat objects should not be changed).
		def getName(self):
			return self.__name




