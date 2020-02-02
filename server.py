#!/usr/bin/python3
import http.server
from http.server import BaseHTTPRequestHandler
import socketserver
import argparse


parser = argparse.ArgumentParser(description='HTTP 1.1 server')

PORT = 8080

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


class Server():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5

    def run(self):
        try:
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                print("serving at port", PORT)
                httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()
            print('\nServer shutted down')


Server().run()