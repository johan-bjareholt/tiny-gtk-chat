import socket
import threading

running = True
connected_clients = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = '127.0.0.1'
port = 1337


class Client(threading.Thread):
	def __init__(self, connection, address):
		threading.Thread.__init__(self)
		self.connection = connection
		self.address = address
		self.connected = True
		self.daemon = True
		self.name = "noname"
		self.subscriptions = []
		self.start()

	def run(self):
		print('Client {} Connected!'.format(self.address))
		connected_clients.append(self)
		chatroom.subscribe(self)

		while self.connected:
			data = self.connection.recv(2048)
			if data[0] == '/':
				command_handler(self, data, chatroom)
			else:
				chatroom.new_message(self, data)
		self.connection.close()

		for channel in self.subscriptions:
			channel.connected.remove(self)

		connected_clients.remove(self)

	def send_data(self, data):
		self.connection.send(data)
		print(data)

class ChatRoom():
	def __init__(self, name):
		self.name = name.lower()
		self.connected = []

	def new_message(self, user, message):
		data = user.name + ": " + message
		for user in self.connected:
			try:
				user.send_data(data)
			except socket.error as e:
				#if e.errno == 32: # Broken Pipe
				#	print(user + " is no longer connected")
				#	user.connected = False
				#else:
				print("Socket error:" + e) 
			except Exception as e:
				print(e)

	def subscribe(self, user):
		self.connected.append(user)
		user.subscriptions.append(self)

def command_handler(user, message, channel):
	message_parameters = message.split(" ")
	if message_parameters[0] == "/username":
		user.name = message_parameters[1]
		user.send_data("Your name was successfully changed to " + message_parameters[1])
	elif message_parameters[0] == "/help":
		user.send_data("Available commands: \n"+
					   "/username [username] - Changes your username\n"+
					   "/help - shows this help message\n")
	else:
		user.send_data("Unknown command!\nType /help for available commands")


def loop():
	print("Binding port")
	sock.bind((server_address, port))
	sock.listen(5)
	print("Listening for connections")
	while running:
		# Accepting new connections
		conn, address = sock.accept()
		print('Client {} found!'.format(address))
		Client(conn, address)


chatroom = ChatRoom("lobby")
loop()