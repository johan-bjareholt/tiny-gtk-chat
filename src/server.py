import socket
import threading

running = True
connected_clients = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = '127.0.0.1'
port = 1337


motd = ("Welcome to Johans tiny-gtk-chat server!\n"+
	   "glhf guise")


class Client(threading.Thread):
	def __init__(self, connection, address):
		threading.Thread.__init__(self)
		self.connection = connection
		self.address = address
		self.connected = True
		self.daemon = True
		self.name = self.address
		self.username = "noname"
		self.subscriptions = []
		self.start()

	def run(self):
		print('Client {} Connected!'.format(self.address))
		connected_clients.append(self)
		self.send_data(motd)
		chatroom.subscribe(self)

		try:
			while self.connected:
				data = self.connection.recv(2048)
				if data:
					if data[0] == '/':
						command_handler(self, data, chatroom)
					else:
						chatroom.new_message(self.username, data)
		except Exception as e:
			print(str(self.address) + " encountered an error!\n" + str(e))

		self.disconnect()

	def disconnect(self):
		self.connected = False
		self.connection.close()
		try:
			for channel in self.subscriptions:
				channel.unsubscribe(self)
			connected_clients.remove(self)
		except ValueError:
			pass
		except Exception as e:
			raise e

	def send_data(self, data):
		try:
			self.connection.send(data)
		except socket.error as e:
			if e[0] == 32: # Broken pipe
				self.disconnect()
			else:
				raise e
		except Exception as e:
			raise e

class ChatRoom():
	def __init__(self, name):
		self.name = name.lower()
		self.connected = []

	def new_message(self, user, message):
		data = user + ": " + message
		for user in self.connected:
			user.send_data(data)
		print(data)

	def subscribe(self, user):
		self.connected.append(user)
		user.subscriptions.append(self)
		self.new_message("Info", user.username + " joined the chatroom")

	def unsubscribe(self, user):
		self.connected.remove(user)
		user.subscriptions.remove(self)
		self.new_message("Info", user.username + " left the chatroom")

def command_handler(user, message, channel):
	message_parameters = message.split(" ")
	if message_parameters[0] == "/username":
		user.username = message_parameters[1]
		user.send_data("Your name was successfully changed to " + message_parameters[1])
	elif message_parameters[0] == "/motd":
		user.send_data(motd)
	elif message_parameters[0] == "/help":
		user.send_data("Available commands: \n"+
					   "/username [username] - changes your username\n"+
					   "/help - shows this help message\n"+
					   "/motd - shows the message of the day\n")
	else:
		user.send_data("Unknown command!\nType /help for available commands")


def listen():
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
listen()