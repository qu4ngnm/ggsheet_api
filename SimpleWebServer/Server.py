from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
from database.db import create_table, signup, check_login
import sys

def read_html_template(path):
    try:
        with open(path) as f:
            file = f.read()
    except Exception as e:
        file = e
    return file

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = './src/html/index.html'
        elif self.path == '/login':
            self.path = './src/html/Login.html'
        elif self.path == '/signup':
            self.path = './src/html/Signup.html'
        try:
            split_path = os.path.splitext(self.path)
            request_extension = split_path[1]
            if request_extension != ".py":
                f = read_html_template(self.path)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(f, 'utf-8'))
            else:
                f = "File not found"
                self.send_error(404,f)
        except:
            f = "File not found"
            self.send_error(404,f)

    def do_POST(self):
        if self.path == '/submit':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                user_name = fields.get("username")[0]
                pass_wd = fields.get("passwd")[0]
                # create table User if it runs first time else not
                create_table()
                # insert record into User table
                signup(user_name, pass_wd)
                html = f"<html><head></head><body><h1>Form data successfully recorded!!!</h1></body></html>"
                self.send_response(200, "OK")
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(html, "utf-8"))

with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()