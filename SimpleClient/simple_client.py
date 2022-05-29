import requests
import argparse

parser = argparse.ArgumentParser(description='Process some HTTP Requests.')
parser.add_argument('-m','--method',metavar='method',required=True, help='method: GET, POST only')
parser.add_argument('-data',metavar='data',type=str, help='Specific data to POST only')
parser.add_argument('-host',metavar='host', required=True, help='Specific host name')
args = parser.parse_args()

method = args.method
data_to_post = args.data
url = args.host

def do_Get(url):
    req = requests.get(url)
    return req.json()

def do_Post(url):
    url_to_post = url + "?" + data_to_post
    req = requests.post(url_to_post)
    return req.json()

def main():
    if method == "GET":
        print(do_Get(url))
    elif method == "POST":
        print(do_Post(url))
if __name__ == "__main__":
    main()