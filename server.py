#!/usr/bin/python3
import http.server
from http.server import BaseHTTPRequestHandler
import socketserver
import argparse
from logger import Logger


parser = argparse.ArgumentParser(description='HTTP 1.1 server')
parser.add_argument('port', type=int, help='port to connections')
parser.add_argument("-o", "--origin",
                    help="Access-Control-Allow-Origin default header",
                    action="store_true")
parser.add_argument("-m", "--methods",
                    help="Access-Control-Allow-Methods default header",
                    action="store_true")

args = parser.parse_args()
PORT = args.port

logger = Logger('.log')


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')
        logger.log_response('GET', str(self.path), str(self.headers))


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
                print("Serving at port", PORT)
                logger.log_start(PORT)
                httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()
            print('\nServer shutted down')
            logger.log_shutdown()


if __name__ == "__main__":
    Server().run()
