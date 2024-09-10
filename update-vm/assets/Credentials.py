import os
from dotenv import load_dotenv

class Credentials:
    def __init__(self):
        load_dotenv()
        self.username = None
        self.password = None

    def collect_data(self):
        self.username = os.getenv('USERNAME_VCLOUD')
        self.password =  os.getenv('PASSWORD_VCLOUD')




