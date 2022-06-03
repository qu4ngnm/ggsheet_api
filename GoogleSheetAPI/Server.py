from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
from database.db import create_table, signup, check_login
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
import gspread

islogin = False
type = 0


# SERVICE_ACCOUNT_FILE = 'key.json'
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# SPREADSHEET_ID = '1eJU4xJgSyHyC2WDGsaVT8J6Mv4nn7fd-OJIS-Tl2Dig'
# creds = None
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# service = build('sheets', 'v4', credentials = creds)
# sheet = service.spreadsheets()
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
        row = cell.row
        worksheet.delete_row(row)
    def update_row(self, name, email):
        cell = worksheet.find(name)
        row = cell.row
        col = cell.col
        worksheet.update_cell(row, col + 1, str(email))
    def write_to_json(self):
        with open('status.json', 'w') as json_file:
            json.dump(self.get_data(), json_file)

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
        # elif self.path == '/getdata'
        #     self.path = 'status.json'
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
                    self.write_to_json()
                    self.path = "status.json"
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
                            self.send_error(404, f)
                    except:
                        f = "File not found"
                        self.send_error(404, f)

                elif method[0] == 'insert':
                    self.insert_data(str(name[0]), str(email[0]))
                    f = """
                    {
                        "Success": "True"
                    }
                    """
                    try:
                        split_path = os.path.splitext(self.path)
                        request_extension = split_path[1]
                        if request_extension != ".py":
                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write(bytes(f, 'utf-8'))
                        else:
                            f = "File not found"
                            self.send_error(404, f)
                    except:
                        f = "File not found"
                        self.send_error(404, f)
                elif method[0] == 'update':
                    self.update_row(str(name[0]), str(email[0]))
                    f = """
                    {
                         "Success": "True"
                    }
                    """
                    try:
                        split_path = os.path.splitext(self.path)
                        request_extension = split_path[1]
                        if request_extension != ".py":
                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write(bytes(f, 'utf-8'))
                        else:
                            f = "File not found"
                            self.send_error(404, f)
                    except:
                        f = "File not found"
                        self.send_error(404, f)
                elif method[0] == 'delete':
                    self.delete_data(str(name[0]))
                    f = """
                    {
                        "Success": "True"
                    }
                    """
                    try:
                        split_path = os.path.splitext(self.path)
                        request_extension = split_path[1]
                        if request_extension != ".py":
                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write(bytes(f, 'utf-8'))
                        else:
                            f = "File not found"
                            self.send_error(404, f)
                    except:
                        f = "File not found"
                        self.send_error(404, f)




with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()

