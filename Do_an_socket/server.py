import socket

HOST = 'localhost'
PORT = 8000
NUM_LISTEN = 5
SIZE = 1024 * 1024
FORMAT = 'utf-8'

def createSocket(port):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((HOST, port))
	s.listen(5)
	return s;

def receive(Client):
	return Client.recv(SIZE).decode(FORMAT)

def isGET(packet):
	return 'GET' in packet

def isPOST(packet):
	return 'POST' in packet

def isVideo(path):
	return '.png' in path or '.jpg' in path or '.ico' in path or '.mp4' in path


def isDocument(path):
	return '.docx' in path or '.pptx' in path or '.xlsx' in path or '.pdf' in path or '.txt' in path or '.pub' in path

def createHeader(path):
	filename = ''
	if '404' not in path: filename = 'headerok.txt'
	elif '404' in path: filename = 'header404.txt'
	readHeader = open(filename)
	header = readHeader.read()
	readHeader.close()
	return header

def response(path, Client):
	header = createHeader(path)
	if isVideo(path) or isDocument(path):
		file_data = open(path, 'rb')
		data = file_data.read()
		send = bytes(header, FORMAT) + data
		client.sendall(send)
		file_data.close()
	else:
		file_data = open(path)
		data = file_data.read()
		send = header + data
		client.sendall(bytes(send, FORMAT))
		file_data.close()

def handleGET(packet, Client):
	path = packet.split('\n')[0].split(' ')[1]
	if path == '/' : path = './index.html'
	else: path = '.' + path
	response(path, Client)

def handlePOST(packet, Client):
	if not isPOST(packet) or 'Username=admin&Password=admin' not in packet: response('./404.html', Client)
	else: response('./info.html', Client)



print('waiting for connection...')

while True:
	s = createSocket(PORT)
	client, addr = s.accept()
	s.close()

	packet = receive(client)
	print('packet received : ', packet)

	if packet != '':
		if isGET(packet): handleGET(packet, client)
		elif isPOST(packet): handlePOST(packet, client)
	client.close()