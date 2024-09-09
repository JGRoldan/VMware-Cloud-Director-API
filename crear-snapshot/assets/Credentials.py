from colorama import Fore, Style

class Credentials:
    def __init__(self):
        self.username = None
        self.password = None

    def collect_data(self):
        self.username = input(f"{Fore.BLUE}[Input]{Style.RESET_ALL} Ingrese el usuario local: ")
        self.password = input(f"{Fore.BLUE}[Input]{Style.RESET_ALL} Ingrese la contraseña: ")




