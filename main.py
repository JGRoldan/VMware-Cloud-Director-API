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

def get_token_authentication(auth, username, password):
    api_version = auth.get_api_version(username, password)
    token = auth.get_token_authentication(username, password, api_version)
    
    return token, api_version

def get_vApps(username, password, token, api_version):
    http = HTTPMethods()
    vApps = http.get_vApps(username, password, token, api_version)
    return vApps

def get_vm(username, password, token, api_version, vApps_list):
    http = HTTPMethods()
    vm = http.get_vm(username, password, token, api_version, vApps_list)
    return vm

def selected_vm(vm_list):
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

def main_code():
    try:
        auth = Authentication() 
        username, password = get_credentials()
        token, api_version = get_token_authentication(auth, username, password)
        vApps_list = get_vApps(username, password, token, api_version)
        vm_list = get_vm(username, password, token, api_version, vApps_list)# output = [{'href': 'id_de_vm', 'name':'vm_name'}]
        while True:
            print(f"\n{Fore.LIGHTGREEN_EX}[Notice]{Style.RESET_ALL} Seleccione una opción de snapshot...")
            option = input(f"\n{Fore.BLUE}[Input]{Style.RESET_ALL} \n 1. Snapshot selectivo. \n 2. Snapshot de todas las VM(s).: \n")

            while True:
                if(option == '1'):
                    print(f"{Fore.BLUE}[Input]{Style.RESET_ALL} VM(s) disponibles: ")
                    print_table(vm_list)
                    selected_vms = selected_vm(vm_list)
                    if selected_vms:
                        clear_screen()
                        print(f"\n{Fore.LIGHTGREEN_EX}[Update]{Style.RESET_ALL} VM(s) a realizar snapshot:")
                        print_table(selected_vms)
                        #HACER LA SNAPSHOT
                        #HACER LA SNAPSHOT
                    else:
                        clear_screen()  # Limpiar la pantalla si la selección fue incorrecta o vacía
                    
                elif(option == '2'):
                    print(f"{Fore.YELLOW}[Progress]{Style.RESET_ALL} Snapshots en progreso...")
                    #HACER LA SNAPSHOT
                    #HACER LA SNAPSHOT
                    break
                else:
                    print(f"{Fore.YELLOW}[Warning]{Style.RESET_ALL} Entrada inválida. Asegúrate de ingresar la opción correcta.")
                    time.sleep(2)
                    clear_screen()  # Limpiar la pantalla si la selección fue incorrecta o vacía
                    break
                
    except Exception as e:
       print(f"{Fore.RED}[Error]{Style.RESET_ALL} Ocurrió un error: {e}")
    
    input(f"\n{Fore.BLUE}[Input]{Style.RESET_ALL} Presione enter para salir...")

if __name__ == '__main__':
    init(autoreset=True)
    main_code()