# Proyecto de Automatizacion de tests para el sitio Parabank

En este repositoro expongo todo lo necesario para entender el funcionamiento y poder correr los tests para el sitio [Parabank](https://parabank.parasoft.com/) o para su version contenerizada usando python, pytest, Selenium y acceso a base de datos.

## Obejetivos del proyecto

- Practicar y demostrar habilidades de automatización de pruebas en diferentes capas (API, UI, base de datos).
- Aprender, comprender y aplicar buenas practicas en estructuración de proyectos de testing automatizado.
- Integrar pruebas automatizadas con Jenkins y reportes con Allure
- Utilizar Docker para fortalecer la modularización y mantenimiento del proyecto. \*?
- ¿como agregar que realice todo en linux y usado VS code? suma poner eso?

## Stack y herramientas

- Lenguaje: Python 3.8
- Framework de testing: `pytest`
- Automatizacion tests UI: `Selenium`
- Automatizacion tests API: `requests` y `jsonschema`
- Acceso a base de datos: `jaydebeapi` y `hsqldb`
- Reportes: `Allure`
- CI: Jenkins, utilizando pipelines con script declarativo.
- Docker

## Estructura del proyecto

```
QA_automation_portfolio
├── LICENSE
├── parabank_API
│   ├── api_clients
│   ├── clients
│   ├── config.py
│   ├── schemas
│   ├── tests
│   └── utils
├── parabank_database
│   ├── db_clients
│   ├── java-lib
│   ├── prueba.py
│   └── tests
├── parabank_front
│   ├── config.json
│   ├── config.py
│   ├── pages
│   └── tests
├── pytest.ini
├── README.md
└── requirements.txt
```

## Objeto de pruebas

Elegi realizar los tests sobre el sitio **parabank** que es una demo de la empresa Parasoft. Este sitio contine una UI funcional y limpia, documentación detallada sobre los endpoints y como realizar requests en un swagger e incluso si se utiliza la version contenerizada o se levanta el sitio en forma local se puede acceder tambien a la base de datos.
Esta posibilidad de tener acceso a tantas capas de un mismo sitio me hizo elegir este sitio para mis pruebas y demostraciones. **(reformular la horacion para no usar dos veces "sitio")**

## Como ejecutar los tests

Instrucciones paso a paso para ejecutar los tests.

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/parabank-qa-automation.git
cd parabank-qa-automation
```

### 2. Setup de entorno virtual

El proyecto fue desarrollado y probado usadno python3.8 por lo cual es recomendable (y tal vez hasta mandatorio) utilizar la misma version de python

    1. Instalar Python3.8

```bash
    apt update
    apt install -y   wget build-essential   libssl-dev zlib1g-dev   libncurses5-dev libncursesw5-dev   libreadline-dev libsqlite3-dev   libgdbm-dev libdb5.3-dev libbz2-dev   libexpat1-dev liblzma-dev tk-dev
    cd /usr/src
    wget https://www.python.org/ftp/python/3.8.18/Python-3.8.18.tgz
    tar xzf Python-3.8.18.tgz
    cd Python-3.8.18
    ./configure --enable-optimizations
    make -j$(nproc)
    make altinstall #para mantner la version de python por defecto
    python3.8 --version
```

    Verificar la instalacion:

```bash
python3.8 --version
```

    Deberias ver:
    *Python 3.8.18*

    2. Crear y activar entorno virtual con python3.8

```bash
    python3.8 -m venv venv-automation
    source venv-automation/bin/activate
```

    3. Instalar dependecias

```bash
    pip install -r requirements.tx
```

### 3. Ejecutar los tests

Los tests deben ejecutarse desde la carpeta raiz del proyecto.

```bash
    python -m pytest -v
```

O si se quiere tener más informacion de la ejecución:

```bash
    python -m pytest -v --log-cli-level=INFO
```

### 4. Generar reportes con Allure

[Allure Report](https://allurereport.org/) es una herramienta oepnsource, multiplataforma y multilenguaje que genera reportes de forma automatizada. Esots reportes son visulamente atractivos, tecnicamente muy útiles y constan de: Dashboard, Métricas, Historico de ejecuciones, Navegación por test, logs, etc.
Para utilizar Allure Reports es necsario instalar la aplicacion en nuestro sistema operativo y además agregar la libreria en nuestro entorno virtual (esto ya lo hicimos con los requirements).

1. Instalar Allure Reports en Ubuntu Linux desde paquetes DEB
   1. Descargar paquete allure-\*.deb desde el [repositorio oficial de Allure](https://github.com/allure-framework/allure2/releases)
   2. Desde la terminal ejecutar
   ```bash
   sudo dpkg -i allure_*.deb
   ```
   3. Comprobar instalacion
   ```bash
   allure --version
   ```
2. Ejecutar los tests y generar archivos para reporte

```bash
    python -m pytest -v --log-cli-level=INFO --alluredir=allure-results
```

3. Generar reporte

```bash
   allure serve allure-results
```

### 5. Integracion con Jenkins

Para Simular un entorno real realicé tambien la integracion de este proyecto con Jenkins. Este se encuentra corriendo en docker.
El trabajo de jenkins realiza:

- Configura variables de entorno
- Realiza un checkout del proyecto desde GitHub
- Activa el entorno virtual e instala dependencias
- Genera el reporte de Allure

1. Crear contenedor con jenkins
   Para levantar el jenkins me base en la imagen de [vdespa](https://vdespa.com/) y creé la mia propia que se puede descargar y crear el contenedor usando:

```bash
    docker run -d --name jenkins-postman \
      -p 8080:8080 -p 50000:50000 \
      --restart=on-failure \
      -v jenkins_home:/var/jenkins_home \
      --env JAVA_OPTS="-Dfile.encoding=UTF8" \
      dario8a/jenkins-postman
```

Con esto le damos un nombre facilmente referenciable a nuestro contenedor, exponemos los puertos, se reiciará automaticamente si se cae, creamos un volumen para persistencia de datos y evitamos algunois problemas de codificación

2. Es necesario instalar Chrome, Firefox o el browser que usaremos para las pruebas de UI
   Para acceder a la consola del contenedor como usuario root
   `bash
        docker exec -it --user root jenkins-postman bash
    `
   Una vez en el contenedor instalar dependencias:
   `bash
        apt update
        apt-get install -y wget gnupg2 curl unzip fonts-liberation libu2f-udev libvulkan1 \
        libxss1 libappindicator3-1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libnss3 \
        libx11-xcb1 libxcb-dri3-0 libgbm1 libdrm2 libxcomposite1 libxdamage1 \
        libxrandr2 libxi6 libglu1-mesa
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
        sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
    `
   Instalar Google Chrome
   `bash
        apt update
        apt install -y google-chrome-stable
    `
   Verificar instalalción
   `bash
        google-chrome --version
    `
   Instalar dependecias extra que son utilizadas para renderizar páginas web, manejar sonido y gestionar procesos internos en las pruebas de UI:
   `bash
        apt install -y libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0
    `

3. Instalar Allure CLI en jenkins
   Desde Administrar Jenkins > Herramientas > instalaciones de Allure Commandline
   Añadir una instalación, usar Instalar Automaticamente.
   Guardar.

4. Crear una nueva tarea tipo pipeline y pegar el contenido del archivo jenkins/Jenkinsfile en el campo Pipeline script

5. Construir la nueva tarea.

### Dockerizar el sitio de Parabank
