import sys, socket, threading
sys.path.append("..")
import irc_main

class SmallMessage:
	def __init__(self, msg, username):
		self.message = msg
		self.username = username
		

class IRC_Client:
	def __init__(self, host, port, username, showMessagesInstant=False):
		self.username = username
		self.connection = socket.create_connection((host, port))
		self.connection.send(irc_main.createMessage(username, "hi"))
		self.showMessagesInstant = showMessagesInstant

		self.messages = []
		threading.Thread(target=self.start_listening).start()

	def start_listening(self):
		while True:
			data = self.connection.recv(1024)
			if data != b"":
				decoded = irc_main.decodeMessage(data)
				if self.showMessagesInstant:
					print(f">> {decoded[2]}: {decoded[1]}")
				self.messages.append(SmallMessage(decoded[2], decoded[1]))

	def send_message(self, msg):
		self.connection.sendall(irc_main.createMessage(self.username, msg))
		print("message sent")