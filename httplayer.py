#!/usr/local/bin/python3
import socket
import os
from urllib.parse import parse_qs

class ResponseGenerator():
	status_codes = {
		'Continue':				 100,
		'OK':					   200,
		'Found':					302,
		'Bad Request':			  400,
		'Not Found':				404,
		'Internal Server Error':	500
	}
	def __init__(self, status, headers = [], body = b''):
		self.status = status
		self.status_code = str(self.status_codes[self.status])
		self.headers = headers
		self.body = body
	def compile(self, chunked = False):
		assert(isinstance(self.body, bytes))
		header = ['HTTP/1.1 ' + self.status_code + ' ' + self.status]
		header.extend([line for line in self.headers])
		header.append('Content-Length: ' + str(len(self.body)))
		msg = '\n'.join(header).encode('utf-8') + b'\n\n' + self.body
		return msg
	def __str__(self):
		try:
			return self.compile().decode('utf-8')
		except:
			return 'not printable'

class RequestHandler():
	def __init__(self, req):
		self.req = [line.replace(chr(13), '') for line in req.decode('utf-8').split( '\n')]

		print(self.req[0])
		self.met, self.arg, self.http_version = self.req[0].split(' ')

		self.body = []
		self.referer = '/'
		for idx, line in enumerate(self.req):
			if line[:8] == 'Referer:':
				self.referer = line[len(''.join(line.split('/')[:3])) + 2:]

			elif line == '':
				self.body = self.req[idx+1:]
		
	#a[len(''.join(a.split('/')[:3])) + 2:]


	def __repr__(self):
		return '\n'.join(self.req)

def socket_init():
	host, port = '', 80
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	s.listen(1)
	return s

def fucked_up():
	return ResponseGenerator('Internal Server Error', body = b'there was an issue with the server')

def recv(s):
	while True:
		try:
			con, addr = s.accept()
			raw_req = con.recv(1024)
			return con, raw_req
		except KeyboardInterrupt:
			print()
			exit()
		except:
			pass

def send(con, res):
	con.sendall(res.compile(chunked = False))
	con.close()
