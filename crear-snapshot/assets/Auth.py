import requests
import json
from colorama import Fore, Style
from requests.auth import HTTPBasicAuth

class AuthenticationError(Exception):
    """Excepción personalizada para errores."""
    pass

class Authentication:
    def __init__(self):
        self.auth_url_api = 'https://vcd.clarocloud.com/api/sessions'
        self.api_version_api = 'https://vcd.clarocloud.com/api/versions'

    def get_api_version(self,username, password):
        response = requests.get(self.api_version_api, auth=HTTPBasicAuth(username, password), headers={'Accept': f'application/*+json;'})
        if response.status_code == 200:
            try:
                json_data = json.loads((response.text))  # Convertir la data a JSON
                supported_versions = json_data.get('versionInfo', {})  # Obtener versionInfo
                version_info_list = supported_versions[-1]  # Obtener ultima version

                if version_info_list:  # Verificar que la lista no esté vacía
                    api_version = version_info_list.get('version')  # Obtener la última versión de la API
                else:
                    raise AuthenticationError('VersionInfo list is empty.')
                
            except Exception as e:
                raise AuthenticationError(f'Error parsing the API version response: {e}')
            
        else:
            raise AuthenticationError(f'Failed to get Api Version with status code {response.status_code}')
                    
        return api_version        

    def get_token_authentication(self, username, password, api_version):
        response = requests.post(self.auth_url_api, auth=HTTPBasicAuth(username, password), headers={'Accept': f'application/*+json;version={api_version}'})
        
        if response.status_code == 200:
            token = response.headers['x-vcloud-authorization']
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Autenticación exitosa.")
        else:
            raise AuthenticationError(f'Fallo la autenticación con codigo de error: {response.status_code}')

        return token
