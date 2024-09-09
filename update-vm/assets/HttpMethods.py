import requests
import json, time
from colorama import Fore, Style
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor

class HTTPError(Exception):
    """Excepción personalizada para errores."""
    pass

class HTTPMethods:
    def __init__(self):
        self.vm_api = 'https://vcd.clarocloud.com/api/vApp/'

       
# Escribir output en un archivo
# with open('output.txt', 'w') as file:
#     json_string = json.dumps(json_data, indent=4)        
#     file.write(json_string)
#     file.write('\n\n')
