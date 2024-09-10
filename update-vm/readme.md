# Modificar RAM y CPU utilizando VMware Cloud Director API

Este proyecto contiene un código en Python para modificar la ram y cpu en entornos VMware utilizando la API de Cloud Director.

- [Modificar RAM y CPU utilizando VMware Cloud Director API](#modificar-ram-y-cpu-utilizando-vmware-cloud-director-api)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Descripción de las Clases y Funciones](#descripción-de-las-clases-y-funciones)
    - [Clase `Credentials`](#clase-credentials)
    - [Clase `Authentication`](#clase-authentication)
    - [Clase `HTTPMethods`](#clase-httpmethods)
    - [Funciones Principales](#funciones-principales)
  - [Ejecución del Código](#ejecución-del-código)
    - [Requisitos](#requisitos)
    - [Ejemplo Caso de Uso](#ejemplo-caso-de-uso)
    - [Modificar RAM](#modificar-ram)


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
- **Método `__init__`**: Define la URL de la request.
- **Método `custom_hardware(username, password, token, api_version)`**: Utiliza el metodo `requests.put(args)` para realizar la petición a la API y realizar la customización del hardware.
Si la respuesta es exitosa, se mostrara un mensaje de `éxito` en pantalla. Si falla, se lanza una excepción `HTTPError`.

### Funciones Principales

- **`get_credentials()`**: Crea una instancia de la clase `Credentials`, solicita las credenciales y las devuelve.
  
- **`get_token_authentication(username, password)`**: Solicita el token de autenticación utilizando las credenciales proporcionadas y devuelve el token.

- **`custom_hardware(username, password, token, api_version)`**: Solicita la modificación del hardware y retorna la respuesta.

- **`main_code()`**: Función principal que coordina la ejecución del programa.

## Ejecución del Código

### Requisitos
- **`Python 3.x`**
- **`Pip3 24.x`**
- **`requests library`**
- **`colorama library`**
- **`Agregar el archivo .env en la raiz con las credenciales con las siguientes variables:`**   USERNAME_VCLOUD=...
PASSWORD_VCLOUD=...

```bash
pip3 install requests colorama
```

### Ejemplo Caso de Uso
1. Añadir un archivo .env en la raiz del proyecto.
2. Realizar los cambios necesarios de customización ([Modificar RAM](#modificar-ram)).
3. Ejecuta el script.
4. El script intentará autenticarte y, si es exitoso, genera la customización del hardware.
5. Fin de Caso de Uso.

### Modificar RAM
1. Tener el ID de la VM.
2. Reemplazar {id} por el ID de la VM.
3. Modificar el body =  """ """, de HttpMethods.py y ejecutar el script.
```xml
<ns2:Item xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns:ns2="http://www.vmware.com/vcloud/v1.5" xmlns:vmext="http://www.vmware.com/vcloud/extension/v1.5" xmlns:vssd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData" xmlns:common="http://schemas.dmtf.org/wbem/wscim/1/common" xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:vmw="http://www.vmware.com/schema/ovf" xmlns:ovfenv="http://schemas.dmtf.org/ovf/environment/1" xmlns:ns9="http://www.vmware.com/vcloud/versions" ns2:type="application/vnd.vmware.vcloud.rasdItem+xml" ns2:href="https://vcd.clarocloud.com/api/vApp/{id}/virtualHardwareSection/memory">
    <rasd:Address xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:AddressOnParent xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:AllocationUnits>byte * 2^20</rasd:AllocationUnits>
    <rasd:AutomaticAllocation xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:AutomaticDeallocation xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:ConfigurationName xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:ConsumerVisibility xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:Description>Memory Size</rasd:Description>

    <!-- Modificamos  ElementName a 8GB = 8192MB-->
    <rasd:ElementName>8192 MB of memory</rasd:ElementName>
    
    <rasd:Generation xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:InstanceID>5</rasd:InstanceID>
    <rasd:Limit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:MappingBehavior xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:OtherResourceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:Parent xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:PoolID xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:Reservation>0</rasd:Reservation>
    <rasd:ResourceSubType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:ResourceType>4</rasd:ResourceType>

    <!--  Modificamos VirtualQuantity  a 8GB = 8192MB-->
    <rasd:VirtualQuantity>8192</rasd:VirtualQuantity>

    <rasd:VirtualQuantityUnits xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
    <rasd:Weight>0</rasd:Weight>
    <ns2:Link rel="edit" href="https://vcd.clarocloud.com/api/vApp/{id}/virtualHardwareSection/memory" type="application/vnd.vmware.vcloud.rasdItem+xml"/>
    <ns2:Link rel="edit" href="https://vcd.clarocloud.com/api/vApp/{id}/virtualHardwareSection/memory" type="application/vnd.vmware.vcloud.rasdItem+json"/>
</ns2:Item>
```

