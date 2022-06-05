from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
from database.db import create_table, signup, check_login
import json
import gspread

islogin = False
type = 0

row_index = 1

gc = gspread.service_account(filename='key.json')
sheet = gc.open_by_key('1eJU4xJgSyHyC2WDGsaVT8J6Mv4nn7fd-OJIS-Tl2Dig')
worksheet = sheet.sheet1

def read_html_template(path):
    try:
        with open(path) as f:
            file = f.read()
    except Exception as e:
        file = e
    return file

class handler(BaseHTTPRequestHandler):
    def get_data(self):
        res = worksheet.get_all_records()
        return res
    def insert_data(self, username, email):
        row_index = worksheet.row_count
        insert_row = [str(username), str(email)]
        worksheet.insert_row(insert_row, row_index)
    def get_row_index(self, name):
        cell = worksheet.find(name)
        return cell.row
    def delete_data(self, name):
        cell = worksheet.find(name)
        if cell is not None:
            row = cell.row
            worksheet.delete_row(row)
            return 1
        else:
            return 0
    def update_row(self, name, email):
        cell = worksheet.find(name)
        if cell is not None:
            row = cell.row
            col = cell.col
            worksheet.update_cell(row, col + 1, str(email))
            return 1
        else:
            return 0
    def write_to_json(self, data):
        with open('sheet_data.json', 'w') as json_file:
            json.dump(data, json_file)

    def status_json(self, data):
        with open('sheet_data.json', 'w') as json_status:
            json.dump(data, json_status)

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
        elif self.path == '/getdata':
            self.path = 'sheet_data.json'
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

        elif self.path == '/action':
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                method = fields.get('method')
                name = fields.get('name')
                email = fields.get('email')
                if method[0] == 'read':
                    self.write_to_json(self.get_data())


                if method[0] == 'insert':
                    self.insert_data(str(name[0]), str(email[0]))
                    status_json = """{"Success":"True"}"""
                    self.status_json(status_json)

                elif method[0] == 'update':
                    self.update_row(str(name[0]), str(email[0]))
                    if self.update_row(str(name[0]), str(email[0])) == 1:
                        status_json = """{"Success":"True"}"""
                        self.status_json(status_json)
                    else:
                        status_json = """{"Success":"False"}"""
                        self.status_json(status_json)

                elif method[0] == 'delete':
                    self.delete_data(str(name[0]))
                    if self.delete_data(str(name[0])) == 1:
                        status_json = """{"Success":"True"}"""
                        self.status_json(status_json)
                    else:
                        status_json = """{"Success":"False"}"""
                        self.status_json(status_json)





with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()

