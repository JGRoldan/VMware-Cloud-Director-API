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
        #self.vdc_id_api = 'https://vcd.clarocloud.com/api/query?type=orgVdc'
        self.vApp_id_api = 'https://vcd.clarocloud.com/api/vApps/query'
        self.vm_api = 'https://vcd.clarocloud.com/api/vApp/'
    
    def make_request(self, url, username, password, token=None, api_version=None, method='GET'):
        headers = {
            'Accept': f'application/*+json;version={api_version}', 
            'x-vcloud-authorization': token
            }
        
        auth = HTTPBasicAuth(username, password)
        if method == 'GET':
            response = requests.get(url, auth=auth, headers=headers)
        elif method == 'POST':
            headersPost = {
                'Content-Type': f'application/vnd.vmware.vcloud.createSnapshotParams+json;', 
                'Accept': f'application/*+json;version={api_version}',
                'x-vcloud-authorization': token
            }           
            body = json.dumps({
                "CreateSnapshotParams": {
                    "xmlns": "http://www.vmware.com/vcloud/v1.5",
                    "name": "Snapshot creado desde script",
                    "Description": "Snapshot creado desde script"
                }
            })
            response = requests.post(url, auth=auth, headers=headersPost, data=body)
            #print(response.text)
            
        if response.status_code in [200, 202]:
            if response.content:  # Verificar si la respuesta tiene contenido
                try:
                    return json.loads(response.text)
                except json.JSONDecodeError as e:
                    raise HTTPError(f'Error parseando respuesta JSON: {e}')
            else:
                return {'status': 'success', 'message': f'Petición exitosa con codigo {response.status_code}'}
        else:
            raise HTTPError(f'Petición fallida con código de error: {response.status_code}')
        
    def get_vApps(self, username, password, token, api_version):
        json_data = self.make_request(self.vApp_id_api, username, password, token=token, api_version=api_version)
        vApp_json = json_data.get('record')
        
        if vApp_json:
            return [item.get('href').split('/')[-1] for item in vApp_json]
        raise HTTPError('La vApp data esta vacia.')

    def get_vm(self, username, password, token, api_version, vApps_list):
        print(f"{Fore.YELLOW}[Progress]{Style.RESET_ALL} Obteniendo datos...")
        result = []

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_vm, vm, username, password, token, api_version, result) for vm in vApps_list]

            for future in futures:
                future.result()  # Esto permite propagar excepciones si ocurren en algún hilo

        return result

    def process_vm(self, vm, username, password, token, api_version, result):
        json_data = self.make_request(f'{self.vm_api}/{vm}', username, password, token=token, api_version=api_version)
        vm_json = json_data.get('children')
        
        if vm_json is not None:
            vm_json_data = vm_json.get('vm')[0]
            result.append({
                'href': vm_json_data['href'].split('/')[-1], 
                'name': vm_json_data['name']
            })
    
    def create_snapshot(self, username, password, token, api_version, vm_list):
        print(f"{Fore.YELLOW}[Progress]{Style.RESET_ALL} Creando snapshots...")
        
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_snapshot, vm, username, password, token, api_version) for vm in vm_list]
            for future in futures:
                future.result()  # Permite propagar excepciones si ocurren en algún hilo

    def process_snapshot(self, vm, username, password, token, api_version):
        try:
            json_data = self.make_request(f'{self.vm_api}/{vm}/action/createSnapshot', username, password, token=token, api_version=api_version, method='POST')
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Snapshot creado para VM: {vm}")
        except Exception as e:
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error creando snapshot para VM: {vm} - {e}")

        
# Escribir output en un archivo
# with open('output.txt', 'w') as file:
#     json_string = json.dumps(json_data, indent=4)        
#     file.write(json_string)
#     file.write('\n\n')
