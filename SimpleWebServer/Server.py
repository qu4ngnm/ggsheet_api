from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi

from supervisor.medusa.auth_handler import get_header

from database.db import create_table, signup, check_login
from random import randint
from datetime import datetime
import logging

islogin = False

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
    def get_Ip_addr(self):
        return self.client_address[0]
    def get_header(self):
        return logging.error(self.headers)
    def get_time(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")
    def data_to_send(self):
        login_time = self.get_time()
        header_data = self.get_header()
        ip_client = self.get_Ip_addr()
        data = ('{"IP_Client": '+ str(ip_client) + ', "HTTP_Header": ' + str(header_data) + ', "Login_Time": '+ str(login_time) + '}')
        return data
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