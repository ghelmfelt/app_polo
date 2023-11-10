# Instalar Docker Desktop en Windows:

Descargar e instalar [Docker Desktop](https://www.docker.com/products/docker-desktop/).

Luego de finalizada la instalación, abrir una terminal y ejecutar el siguiente comando:

    wsl --update

Ejecutar la aplicación de **Docker Desktop**

Ahora ejecutamos el siguiente comando para asegurarnos que **docker** esta funcionando.

    docker run hello-world

# Descargar archivos desde el repositorio de GitHub:

Crear una carpeta en donde se desea descargar los archivos.
Abrir una terminal en esa ubicación en ejecutar el siguiente comando:

    git clone https://github.com/nativob40/app_polo.git



# Correr archivo docker-compose:
Abrir una terminal y ubicarse dentro de la carpeta donde se encuentra el archivo docker-compose.yml y correr el siguiente comando.

    docker-compose up

ahora si corres el siguiente comando

    docker container ls

debería mostrar algo similar a esto

|CONTAINER_ID  |IMAGE                   |COMMAND               |CREATED       |STATUS       |PORTS                                               |NAMES         |
|--------------|------------------------|----------------------|--------------|-------------|----------------------------------------------------|--------------|
|9afdd516fb76  |grafana/grafana         |"/run.sh"             |23 seconds ago|Up 22 seconds|0.0.0.0:3000->3000/tcp                              |grafana-server|
|08945776ed09  |telegraf:1.27           |"/entrypoint.sh tele…"|23 seconds ago|Up 22 seconds|8092/udp, 8125/udp, 8094/tcp, 0.0.0.0:8125->8125/tcp|telegraf      |
|2cedcd1ca20f  |eclipse-mosquitto:2.0.17|"/docker-entrypoint.…"|23 seconds ago|Up 22 seconds|0.0.0.0:1883->1883/tcp, 0.0.0.0:9001->9001/tcp      |mosquitto     |
|a708f57ea341  |influxdb:2.7            |"/entrypoint.sh infl…"|23 seconds ago|Up 23 seconds|0.0.0.0:8086->8086/tcp                              |influxdb      |

# Acceso a las Interfaces:
* ## InfluxDB:
    Dirígete a la página [http://localhost:8086](http://localhost:8086/signin)

    **User**: *admin*

    **Password**: *adminadmin*

* ## Grafana:
    Dirígete a la página [http://localhost:3000](http://localhost:3000)

    **User**: *admin*

    **Password**: *admin*

# Copiar archivos a la placa:
### Conexión por SSH:
  
    ssh polo@radxa-zero

**password:** *polo1234*

### Copiar archivo por SSH:

Abrir una terminal y ubicarse en la carpeta **APP_POLO** y ejecutar el siguiente comando:

    scp app polo@radxa-zero:

Esto copia la carpeta **app** y todo sus archivos dentro de la placa.

# Información adicional:

* ### Format Data:

El formato en el que se debe enviar la información es el siguiente:

    {"Board1":{"SENSOR":1,"HR":0,"DATETIME":"2023-09-25 13:40:38","LAT":40.60183366666667,"LON":8.562767666666668,"SPEED":0.39,"MAXSPEED":0.39,"TOTAL-DISTANCE":0.0002265709064357303}}

En caso de querer enviar datos sin la placa, se puede hacer conectandonos al container. Para ello, abrimos una terminal y ejecutando el siguiente comando:

    docker exec -it mosquitto "sh" 

Una vez dentro del container, copiamos el mensaje que figura arriba y le damos **Enter**.

* ### Eliminar todo:

Abrir una terminal y ubicarse en la carpeta **APP_POLO** y ejecutar los siguientes comandos:

* Primero, para detener todos los containers.

        docker-compose down

* Segundo, para eliminar todo lo relacionado al proyecto (containers, imágenes, red,etc)

        docker system prune -a