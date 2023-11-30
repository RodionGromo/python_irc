from socketClient import IRC_Client
import time, tkinter, threading

client = None

window = tkinter.Tk()
msg_var = tkinter.Variable()

def readMessages():
	while True:
		msgs = []
		for msg in client.messages:
			msgs.append(f"{msg.username}: {msg.message}")
		msg_var.set(msgs)
		time.sleep(.4)

def sendMessage():
	msg = msg_entry.get()
	if msg != "" or msg != " ":
		client.send_message(msg)

def connectToServer():
	global client
	if username_entry.get() != " " or username_entry.get() != "":
		client = IRC_Client("91.245.227.230", 4316, username_entry.get())
		threading.Thread(target=readMessages).start()
		msg_send["state"] = "normal"
		username_entry["state"] = "disabled"
		connect_button["state"] = "disabled"

window.geometry("305x400")
window.title("IRC чат")

for r in range(4): window.rowconfigure(index=r, weight=1)
for c in range(3): window.rowconfigure(index=c, weight=1)

username_entry = tkinter.Entry()
username_entry.grid(column=0, row=0, columnspan=3)
connect_button = tkinter.Button(text="Войти", command=connectToServer)
connect_button.grid(column=3,row=0)

msg_box = tkinter.Listbox(width=50, height=20, listvariable=msg_var)
msg_box.grid(row=1, column=0, columnspan=4, rowspan=2)
msg_entry = tkinter.Entry()
msg_entry.grid(column=0, row=4, columnspan=3)
msg_send = tkinter.Button(text="Отправить", command=sendMessage)
msg_send.grid(column=3, row=4, columnspan=1)
msg_send["state"] = "disabled"

window.mainloop()