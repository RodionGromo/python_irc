import socketServer

server = socketServer.IRC_Server("localhost", 7761)
server.bootstrap()

while True:
	pass

