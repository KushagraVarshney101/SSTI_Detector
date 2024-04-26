import optparse
import requests
import json
from urllib.parse import urlparse
from colorama import Fore
import pyfiglet
import time

parser = optparse.OptionParser()
parser.add_option("-u", dest="domain", help="Enter URL")
parser.add_option("--post", help="POST Request")
parser.add_option("--get", help="GET Request")
parser.add_option("-p", dest="params", help="Enter Parameter")
parser.add_option("-f", dest="file", help="Scan file e.g urls.txt")
output, args = parser.parse_args()

print(pyfiglet.figlet_format("SSTI SCANNER"))

def replace_param_value(url, payload):
    parsed_url = urlparse(url)
    query = parsed_url.query
    if len(query) == 0:
        return query
    try:
        queries = query.split("&")
        for i in queries:
            param_val = i.split("=")[1]
            query = query.replace(f"={param_val}", f"={payload}")
    except:
        pass
    return query

def generate_payload_url(url, payload):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    path = parsed_url.path
    query = replace_param_value(url, payload)
    fragment = parsed_url.fragment
    if len(urlparse(url).query) == 0:
        return f"{scheme}://{netloc}{path}{query}{fragment}"
    return f"{scheme}://{netloc}{path}?{query}{fragment}"

def load_payloads(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    print(Fore.BLUE + f"[+]{len(data)} PAYLOADS LOADED")
    return data

def scan_get_request(url):
    data = load_payloads("Sample_Payloads.json")
    for payload_data in data:
        payload = payload_data['payload']
        expected_output = payload_data['output']
        final_url = generate_payload_url(url, payload)
        response = requests.get(final_url).text
        if isinstance(expected_output, list):
            for output in expected_output:
                if output in response:
                    print(Fore.RED + f"[+] VULNERABLE\nURL:{final_url}\n------------------")
                    continue
        else:
            if expected_output in response:
                print(Fore.RED + f"[+] VULNERABLE\nURL:{final_url}\n----------------------")

def scan_post_request(url, params):
    data = load_payloads("Sample_Payloads.json")
    for payload_data in data:
        final_params = {}
        for p in params:
            final_params[p] = payload_data["payload"]
        response = requests.post(url, data=final_params).text
        if isinstance(payload_data['output'], list):
            for output in payload_data['output']:
                if output in response:
                    print(Fore.RED + f"[+] VULNERABLE\nURL:{url}\nPAYLOAD:{payload_data['payload']}\n------------------")
                    continue
        else:
            if payload_data['output'] in response:
                print(Fore.RED + f"[+] VULNERABLE\nURL:{url}\nPAYLOAD:{payload_data['payload']}")
        final_params = {}

if output.post:
    try:
        params_list = output.params.split(",")
    except:
        params_list = output.params
    finally:
        scan_post_request(output.domain, params_list)
elif output.file:
    with open(output.file, "r") as url_file:
        urls = url_file.read().split()
        for url in urls:
            print(Fore.BLUE + f"[+] TESTING {url}")
            scan_get_request(url)
elif output.get:
    scan_get_request(output.domain)
