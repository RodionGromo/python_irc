''' 
### Interaction ID's
1 - new message
2 - new user
3 - user left
'''

def decodeMessage(msg: bytes) -> tuple:
	'''
	Decodes and returns a tuple: (interactionId: int, userid: str, any: str)
	'''
	data = msg.decode("utf-8").split(chr(1))
	return (ord(data[0])-42, data[1], data[2])

def createMessage(userID: str, message: str) -> bytes:
	return _encodePattern(1, _createRawMessage(message, userID))

def _intToByte(n: int) -> bytes:
	return bytes(chr(n), "utf-8")

def _createRawMessage(msg: str, uid: str) -> bytes:
	return bytes(uid, "utf-8") + _intToByte(1) + bytes(msg, "utf-8")

def _encodePattern(interactionID: int, data: str) -> bytes:
	return _intToByte(interactionID+42) + _intToByte(1) + data 
