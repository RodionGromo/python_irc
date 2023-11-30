import socket, threading, sys, time
sys.path.append("..")
import irc_main

class Client:
	def __init__(self, sock: socket.socket, userid: str):
		self.sock = sock
		self.userid = userid

class Message:
	def __init__(self, fromuser, msg):
		self.fromuser = fromuser
		self.message = msg
		self.sent_to_users = []

class IRC_Server:
	def __init__(self, host: str, port: int):
		self.addr = (host, port)
		self.serverSock = None
		self.clients = []
		self.messages = []

	def bootstrap(self) -> None:
		print("[Server] Started bootstraping")
		self.serverSock = socket.create_server(self.addr)
		self.enable()

	def listen_to_client(self, client: Client):
		print("[Server] >> Started listening to", client.userid)
		while True:
			try:
				data = client.sock.recv(1024)
			except ConnectionResetError:
				print("[Server] >> Client",client.userid,"forced disconnecting")
				self.clients.remove(client)
				break

			print(">> got data", data)
			if data != b"":
				parsedData = irc_main.decodeMessage(data)
				print(">> parse:", parsedData)
				self.messages.append(Message(parsedData[1], parsedData[2]))
			else:
				print("[Server] << Client",client.userid,"disconnected")
				self.clients.remove(client)
				break

	def send_messages_to_clients(self):
		print("[Server] Started sending messages to users")
		while True:
			for msg in self.messages:
				msg_sentToAll = True
				for client in self.clients:
					if client.userid not in msg.sent_to_users:
						msg_sentToAll = False
						msg.sent_to_users.append(client.userid)
						client.sock.send(irc_main.createMessage(msg.fromuser, msg.message))
				if msg_sentToAll:
					self.messages.remove(msg)
			time.sleep(1)

	def listen_to_new_connections(self):
		print("[Server] Listening to new connections")
		while True:
			new_con = self.serverSock.accept()
			userdata = irc_main.decodeMessage(new_con[0].recv(4096))
			new_client = Client(new_con[0], userdata[1])
			if new_client not in self.clients:
				self.clients.append(new_client)
				threading.Thread(target=self.listen_to_client, args=(new_client,)).start()


	def enable(self) -> None:
		self.serverSock.listen()
		threading.Thread(target=self.listen_to_new_connections).start()
		threading.Thread(target=self.send_messages_to_clients).start()
		print('[Server] Bootstraping complete')
		
