from colorama import init, Fore, Style
from assets.Credentials import Credentials
from assets.Auth import Authentication
from assets.HttpMethods import HTTPMethods

def get_credentials():
    credential = Credentials()
    credential.collect_data()
    
    username = credential.username
    password = credential.password
    
    return username, password

def get_token_and_version(auth, username, password):
    api_version = auth.get_api_version(username, password)
    token = auth.get_token_authentication(username, password, api_version)
    
    return token, api_version

def custom_hardware(username, password, token, api_version):
    http = HTTPMethods()
    return http.custom_hardware(username, password, token, api_version)

def main():
    try:
        auth = Authentication()
        username, password = get_credentials()
        token, api_version = get_token_and_version(auth, username, password)
        vm_data = custom_hardware(username, password, token, api_version)
                
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Ocurrió un error: {e}")    
    input(f"\n{Fore.BLUE}[Input]{Style.RESET_ALL} Presione enter para salir...")

if __name__ == '__main__':
    init(autoreset=True)
    main()