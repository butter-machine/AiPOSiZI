#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse


parser = argparse.ArgumentParser(description='HTTP 1.1 server')

PORT_NUMBER = 8080

class ServerHandler(HTTPServer):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write("Hello World !")
		return


class Server():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5

    def run(self):
        server = HTTPServer(('', PORT_NUMBER), ServerHandler)
        
        try:
            print('Serving at 8000')
            server.serve_forever()
        except KeyboardInterrupt:
            pass

        server.server_close()
        print('\nServer closed')


Server().run()