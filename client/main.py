from socketClient import IRC_Client
import time

username = input("enter username:\n> ")

client = IRC_Client("localhost", 7761, username, showMessagesInstant=True)

while True:
	client.send_message(input("write a message:\n> "))
	print("Messages:")
	for msg in client.messages:
		print(f"{msg.username}: {msg.message}")
	print()