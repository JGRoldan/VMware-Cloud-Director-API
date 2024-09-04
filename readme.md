# Creación de snapshot utilizando VMware Cloud Director API

Este proyecto contiene un código en Python para la creación de snapshots en entornos VMware utilizando la API de Cloud Director.

- [Creación de snapshot utilizando VMware Cloud Director API](#creación-de-snapshot-utilizando-vmware-cloud-director-api)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Descripción de las Clases y Funciones](#descripción-de-las-clases-y-funciones)
    - [Clase `Credentials`](#clase-credentials)
    - [Clase `Authentication`](#clase-authentication)
    - [Clase `HTTPMethods`](#clase-httpmethods)
    - [Funciones Principales](#funciones-principales)
  - [Ejecución del Código](#ejecución-del-código)
    - [Requisitos](#requisitos)
    - [Ejemplo Caso de Uso](#ejemplo-caso-de-uso)


## Estructura del Proyecto

- **`main.py`**: Contiene la clase `Main` para la llamada a las subclases y su posterior gestión.
- **`assets/Credentials.py`**: Contiene la clase `Credentials` para obtener las credenciales del usuario.
- **`assets/Authentication.py`**: Contiene la clase `Authentication` que maneja la autenticación y obtiene el token desde la API.
- **`assets/HttpMethods.py`**: Contiene la clase `HttpMethods` que maneja las peticiones HTTP hacia la API.

## Descripción de las Clases y Funciones

### Clase `Credentials`
Esta clase se utiliza para obtener el nombre de usuario y la contraseña del usuario local.

- **Método `__init__`**: Inicializa las variables `username` y `password`.
- **Método `collect_data()`**: Solicita al usuario que ingrese su nombre de usuario y contraseña.

### Clase `Authentication`
Esta clase gestiona la autenticación del usuario mediante una solicitud a una API externa y obtiene un token de autenticación.

- **Método `__init__`**: Define la URL de autenticación.
- **Método `get_token_authentication(username, password)`**: Realiza una solicitud `POST` a la API para autenticar al usuario con las credenciales proporcionadas. Si la autenticación es exitosa, se devuelve el token de autorización. Si falla, se lanza una excepción `AuthenticationError`.

### Clase `HTTPMethods`
- **Método `__init__`**: Define la URL de las requests.
- **Método `make_request(url, username, password, token=None, api_version=None, method='GET')`**: Gestor de solicitudes `HTTP` a la API. Si la respuesta es exitosa, se devuelve un diccionario. Si falla, se lanza una excepción `HTTPError`.
- **Método `get_vApps(username, password, token, api_version)`**: Utiliza el metodo `make_request(...args)`. Si la respuesta es exitosa, se devuelve un array con el identificador de la vApp. Si falla, se lanza una excepción `HTTPError`.
- **Método `get_vm(username, password, token, api_version, vApps_list)`**: Utiliza el metodo `make_request(args)` y ThreadPoolExecutor para ejecutar el método `process_vm(...args)` en paralelo para cada elemento en vApps_list.
Si la respuesta es exitosa, se devuelve un diccionario con el identificador de la VM y su nombre. Si falla, se lanza una excepción `HTTPError`.
- **Método `create_snapshot(self, username, password, token, api_version, vm_list)`**: Utiliza el metodo `make_request(args)` y ThreadPoolExecutor para ejecutar el método `process_snapshot(...args)` en paralelo para cada elemento en vm_list.
Si la respuesta es exitosa, se crea la snapshot correctamente. Si falla, se lanza una excepción `HTTPError`.

### Funciones Principales

- **`get_credentials()`**: Crea una instancia de la clase `Credentials`, solicita las credenciales y las devuelve.
  
- **`get_token_authentication(username, password)`**: Solicita el token de autenticación utilizando las credenciales proporcionadas y devuelve el token.
- **`get_vApps(username, password, token, api_version)`**: Solicita las vApps disponibles y retorna su ID.
- **`get_vm(username, password, token, api_version, vApps_list)`**: Solicita las VM(s) disponibles y retorna su nombre/id en un diccionario. `[{'href': 'vm-XXX-YYY-ZZZ, 'name':'VM_1'}]`
- **`take_snapshots(username, password, token, api_version, selected_vms=None, vm_list=None)`**: Solicita al metodo `HttpMethos` generar las snapshots correspondientes.

- **`main_code()`**: Función principal que coordina la ejecución del programa.

## Ejecución del Código

### Requisitos
- **`Python 3.x`**
- **`Pip3 24.x`**
- **`requests library`**
- **`colorama library`**
- **`tabulate library`**
```bash
pip3 install requests colorama tabulate
```

### Ejemplo Caso de Uso
1. Ejecuta el script.
2. Ingresa el nombre y contraseña de usuario.
3. El script intentará autenticarte y, si es exitoso, solicitara que queres realizar.
4. Seleccionar si queres realizar una snapshot selectiva o de todas las VM(s)
5. En caso de que selecciones la primer opción, tenes que elegir que VM(s) queres realizar el snapshot. Caso contrario, generara una snapshot de todas las VM(s)
6. Fin de Caso de Uso.

