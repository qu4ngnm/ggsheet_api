from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
import json
from database.db import create_table, signup, check_login
from random import randint
from datetime import datetime
import logging

islogin = False
type = 0
def read_html_template(path):
    try:
        with open(path) as f:
            file = f.read()
    except Exception as e:
        file = e
    return file

class handler(BaseHTTPRequestHandler):
    def gen_token(self):
        return "".join(str(randint(1, 9)) for _ in range(25))
    def get_method(self):
        if type == 0:
            return "GET"
        elif type == 1:
            return "POST"
    def get_Ip_addr(self):
        return self.client_address[0]
    def get_header(self):
        return self.headers
    def get_time(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")
    def data_to_send(self):
        data = {
            "method": str(self.get_method()),
            "ip": str(self.get_Ip_addr()),
            "header": str(self.get_header()),
            "time": str(self.get_time())
        }
        return data
    def write_json(self):
        with open("info.json", "w") as json_out:
            json.dump(self.data_to_send(), json_out)
    def do_GET(self):
        if self.path == '/':
            self.path = './src/html/index.html'
        elif self.path == '/login':
            self.path = './src/html/Login.html'
        elif self.path == '/signup':
            self.path = './src/html/Signup.html'
        elif self.path == '/forgotpwd':
            self.path = './src/html/ForgotPwd.html'
        elif self.path == '/home' and islogin == True:
            self.path = './src/html/singnedIn.html'
        elif self.path == '/getjson':
            self.path = 'info.json'
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
        global is_Login
        is_Login = False
        if self.path == '/submit':
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                username = fields.get("username")[0]
                passwd = fields.get("password")[0]
                # create table User if it runs first time else not
                create_table()
                # insert record into User table
                signup(username, passwd)

                html = "<html><head></head><body><div> Create account successfully !!</div><a href='/login'>Login now</a></body></html>"
                self.send_response(200, "OK")
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(html, "utf-8"))

        elif self.path == '/loginform':
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                username = fields.get("username")[0]
                passwd = fields.get("password")[0]
                if check_login(username, passwd) == 1:
                    user_token = self.gen_token()
                    global islogin
                    islogin = True
                    html = "<html><head></head><body><h1>Login successfully !!!</h1><a href='/home'>Go to HomePage</a></body></html>"
                    self.write_json()
                    self.send_response(200, "OK")
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(bytes(html, "utf-8"))
                else:
                    html = "<html><head></head><body><h1>Login Failed !!! Please try again</h1></body></html>"
                    self.send_response(401, "OK")
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(bytes(html, "utf-8"))

with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()

