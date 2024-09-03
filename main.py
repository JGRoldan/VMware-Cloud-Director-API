import os
import time
from colorama import init, Fore, Style
from tabulate import tabulate
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

def fetch_vms(username, password, token, api_version):
    http = HTTPMethods()
    vApps_list = http.get_vApps(username, password, token, api_version)
    return http.get_vm(username, password, token, api_version, vApps_list)

def select_vms(vm_list):
    user_input = input(f'{Fore.BLUE}[Input]{Style.RESET_ALL} Selecciona las VMs a realizar snapshots separadas por ",": ')

    # Verificar si el usuario ingresó algo
    if not user_input.strip():  # Si la entrada está vacía o contiene solo espacios en blanco
        print(f"{Fore.YELLOW}[Warning]{Style.RESET_ALL} No seleccionaste ninguna VM. Por favor, ingresa una VM.")
        time.sleep(2)
        return

    # Convertir la entrada en una lista de enteros
    try:
        selected_ids = [int(x.strip()) for x in user_input.split(',')]
    except ValueError:
        print(f"{Fore.YELLOW}[Warning]{Style.RESET_ALL} Entrada inválida. Asegúrate de ingresar números separados por comas.")
        time.sleep(2)
        return
    
    # Filtrar las vm seleccionadas
    selected_vms = [vm_list[i] for i in selected_ids if i < len(vm_list)]

    # Verificar si se seleccionó alguna VM válida
    if not selected_vms:
        print(f"{Fore.YELLOW}[Warning]{Style.RESET_ALL} No se seleccionó ninguna VM válida.")
        time.sleep(2)
        return

    return selected_vms

def print_table(data): 
    vapp_names_id = [[index, entry['name']] for index, entry in enumerate(data)]
    table = tabulate(vapp_names_id, headers=["ID", "Nombre de VM"], tablefmt="grid")
    print(table)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def take_snapshots(username, password, token, api_version, selected_vms=None, vm_list=None):
    http = HTTPMethods()
    if selected_vms:
        print(f"\n{Fore.LIGHTGREEN_EX}[Update]{Style.RESET_ALL} VM(s) seleccionadas para snapshot:")
        print_table(selected_vms)
        print(f"{Fore.YELLOW}[Progress]{Style.RESET_ALL} Realizando snapshots de las VM(s) seleccionadas...")
        vm_href = [entry['href'] for entry in selected_vms]
        create_snapshot = http.create_snapshot(username, password, token, api_version, vm_href)
        return
            
    elif vm_list:
        print(f"{Fore.YELLOW}[Progress]{Style.RESET_ALL} Realizando snapshots de todas las VM(s)...")
        vm_href = [entry['href'] for entry in vm_list]
        create_snapshot = http.create_snapshot(username, password, token, api_version, vm_href)
        return
        
def display_menu():
    print(f"\n{Fore.LIGHTGREEN_EX}[Notice]{Style.RESET_ALL} Seleccione una opción de snapshot...")
    print(f"\n{Fore.BLUE}[Input]{Style.RESET_ALL} \n 1. Snapshot selectivo. \n 2. Snapshot de todas las VM(s).")
    return input(f"\n{Fore.BLUE}[Input]{Style.RESET_ALL} Opción: ")

def main():
    try:
        auth = Authentication()
        username, password = get_credentials()
        token, api_version = get_token_and_version(auth, username, password)
        vm_list = fetch_vms(username, password, token, api_version)
        
        while True:
            clear_screen()
            option = display_menu()
            if option == '1':
                print_table(vm_list)
                selected_vms = select_vms(vm_list)
                take_snapshots(username, password, token, api_version, selected_vms=selected_vms)
                break
            elif option == '2':
                take_snapshots(username, password, token, api_version, vm_list=vm_list)
                break
            else:
                print(f"{Fore.YELLOW}[Warning]{Style.RESET_ALL} Entrada inválida. Asegúrate de ingresar la opción correcta.")
                time.sleep(2)
                
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Ocurrió un error: {e}")    
    input(f"\n{Fore.BLUE}[Input]{Style.RESET_ALL} Presione enter para salir...")

if __name__ == '__main__':
    init(autoreset=True)
    main()