# Proyecto de Automatización de tests para el sitio ParaBank

En este repositoro expongo todo lo necesario para entender el funcionamiento y poder correr los tests para el sitio [ParaBank](https://parabank.parasoft.com/) o su version contenerizada usando python, pytest, Selenium y acceso a base de datos.

### Sobre mí:

Soy QA Manual and Automation y mi nombre es OCHOA, Dario. He trabajado en proyectos de Automotive, Android, Sistemas Operativos basados en Linux y Plataformas bancarias.
💼 LinkedIn: [Dario OCHOA](https://www.linkedin.com/in/dario-ochoa/)

## Objetivos del proyecto

- Practicar y demostrar habilidades de automatización de pruebas en diferentes capas: API, interfaz gráfica (UI) y base de datos.
- Aprender, aplicar y documentar buenas prácticas en estructuración de proyectos de testing automatizado.
- Integrar pruebas automatizadas en un pipeline CI/CD con Jenkins y reportes con Allure
- Utilizar Docker para facilitar la modularización y mantenimiento del entorno de pruebas.
- Desarrollar el proyecto íntegramente en un entorno Linux utilizando Visual Studio Code como editor principal.

## Stack y herramientas

- Lenguaje: Python 3.8
- Framework de testing: `pytest`
- Automatización tests UI: `Selenium` y `webdriver-manager`
- Automatizacion tests API: `requests` y `jsonschema`
- Acceso a base de datos: `JayDeBeApi` y `hsqldb`
- Reportes: `Allure`
- CI: Jenkins, utilizando pipelines con script declarativo.
- Docker

## Estructura del proyecto

```
QA_automation_portfolio
├── common
│   ├── config.json
│   └── fixtures
├── jenkins
│   └── Jenkinsfile
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
│   ├── expected_schema
│   ├── java-lib
│   ├── prueba.py
│   └── tests
├── parabank_front
│   ├── config.json
│   ├── config.py
│   ├── front_utils
│   ├── pages
│   └── tests
├── pytest.ini
├── README.md
├── requirements.txt
└── test_robustez.sh

```

## Objeto de pruebas

Elegi **ParaBank** que es un sitio-demo de la empresa Parasoft. Este sitio contine una UI funcional y limpia, documentación detallada sobre los endpoints e incluso si se utiliza la version contenerizada o se levanta el sitio en forma local se puede acceder tambien a la base de datos. Esto permite realizar pruebas en todas las capas y E2E

## Como ejecutar los tests

Instrucciones paso a paso para ejecutar los tests.

### 1. Clonar el repositorio

```bash
    git clone https://github.com/tu_usuario/parabank-qa-automation.git
    cd parabank-qa-automation
```

### 2. Dockerizar el sitio de ParaBank

Para poder realizar tests a la base de datos del sitio es necesario tener el sitio de parabank corriendo en forma local, la forma más simple de lograr esto es usando el contenedor proporcionado por Parasoft y conectarlo a la red red virtual de docker llamada qa-net para luego poder acceder a estos recursos desde el contenedor de Jenkins.

1. Crear la red virtual de Docker

```bash
    docker network create qa-net
```

2. Crear contenedor dandole un nombre, sumandolo a la red virtual de docker qa-net y exponer los puertos:

```bash
    docker run -d \
  --name parabank-site \
  --network qa-net \
  -p 8081:8080 \ # UI + API
  -p 9001:9001 \ # HSQLDB
  -p 61616:61616 \
  parasoft/parabank
```

3. Verificaciones.
   Contenedor:

```bash
    docker ps --filter name=parabank-site
```

    Acceso al sitio web:

```bash
    curl -I http://localhost:8081/parabank
```

    Acceso a la base de datos:

```bash
    nc -zv localhost 9001
```

### 3. Configuración de entorno virtual

El proyecto fue desarrollado y probado usando python3.8 por lo cual es recomendable (y tal vez hasta mandatorio) utilizar la misma version de python

    1. Instalar Python3.8

```bash
    apt update
    apt install -y wget build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev
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

    2. Crear y activar entorno virtual con python3.8

```bash
    python3.8 -m venv venv-automation
    source venv-automation/bin/activate
```

    3. Instalar dependecias

```bash
    pip install -r requirements.txt
```

### 4. Ejecutar los tests

Los tests deben ejecutarse desde la carpeta raiz del proyecto.

```bash
    python -m pytest -v
```

O si se quiere tener más informacion de la ejecución:

```bash
    python -m pytest -v --log-cli-level=INFO
```

Para jecutar los tests separados por capa:

```bash
    python -m pytest -m api -v
    python -m pytest -m database -v
    python -m pytest -m ui -v
```

### 5. Generar reportes con Allure

[Allure Report](https://allurereport.org/) es una herramienta open source, multiplataforma y multilenguaje que genera reportes de forma automatizada. Esots reportes son visulamente atractivos, tecnicamente útiles y constan de: Dashboard, Métricas, Historico de ejecuciones, Navegación por test, logs, etc.
Para utilizar Allure Reports es necsario instalar la aplicacion en nuestro sistema operativo y además agregar la libreria en nuestro entorno virtual (esto último ya lo hicimos con los requirements).

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

### 6. Integracion con Jenkins

Para Simular un entorno real realicé tambien la integracion de este proyecto con Jenkins. Este se encuentra corriendo en un contendor docker.
La tarea de jenkins realiza las siguietens subtareas:

- Configura variables de entorno
- Realiza un checkout del proyecto desde GitHub
- Activa el entorno virtual e instala dependencias
- Ejecuta las suites de tests
- Genera y publica el reporte de Allure

1. Crear contenedor con jenkins
   Para levantar el jenkins me base en la imagen de [vdespa](https://vdespa.com/) y creé la mia propia que se puede descargar y crear el contenedor usando:

```bash
    docker run -d --name jenkins-postman \
    --network qa-net \
    -p 8080:8080 -p 50000:50000 \
    --restart=on-failure \
    -v jenkins_home:/var/jenkins_home \
    --env JAVA_OPTS="-Dfile.encoding=UTF8" \
    dario8a/jenkins-postman
```

Ingresar a: http://localhost:8080/ y realizar configuraciones iniciales.

Con esto le damos un nombre facilmente referenciable a nuestro contenedor, exponemos los puertos, se reiciará automaticamente si se cae, creamos un volumen para persistencia de datos y evitamos algunos problemas de codificación

2. También es necesario instalar Chrome, Firefox o el browser que usaremos para las pruebas de UI
   Para acceder a la consola del contenedor como usuario root

```bash
    docker exec -it --user root jenkins-postman bash
```

    Una vez en el contenedor instalar dependencias:

```bash
    apt update
    apt install -y wget gnupg2 curl unzip fonts-liberation libu2f-udev libvulkan1 \
    libxss1 libappindicator3-1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libnss3 \
    libx11-xcb1 libxcb-dri3-0 libgbm1 libdrm2 libxcomposite1 libxdamage1 \
    libxrandr2 libxi6 libglu1-mesa
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
```

        Instalar Google Chrome

```bash
    apt update
    apt install -y google-chrome-stable
```

        Verificar instalalción

```bash
    google-chrome --version
```

        Instalar dependecias extra que son utilizadas para renderizar páginas web, manejar sonido y gestionar procesos internos en las pruebas de UI:

```bash
    apt install -y libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0
```

3. Instalar Allure CLI en jenkins
   Desde Administrar Jenkins > Herramientas > instalaciones de Allure Commandline
   Añadir una instalación, usar Instalar Automaticamente.
   Guardar.

4. Crear una nueva tarea tipo pipeline y pegar el contenido del archivo jenkins/Jenkinsfile en el campo Pipeline script.
   Este Jenkinsfile define el pipeline de integración continua para ejecutar las pruebas automatizadas, generar los reportes con Allure y manejar el entorno de ejecución con Docker.

5. Construir la nueva tarea.

### Mejoras futuras

#### Ejecución selectiva de pruebas

- ~~Agregar `markers` a los tests para permitir ejecutar subconjuntos específicos: API, UI o base de datos~~ Listo
- Permitir seleccionar el ambiente de ejecución: entorno online público o entorno contenerizado local.

#### Cobertura de pruebas

- ~~Agregar más pruebas automatizadas para la capa de UI.~~ Listo
- ~~Ampliar los tests de validación y consulta sobre la base de datos.~~ Listo

#### Integración y despliegue

- Crear una imagen Docker personalizada para Jenkins con Python 3.8 preinstalado.
- Automatizar la ejecución de pruebas por rama o Pull Request en Jenkins.
- Publicar los reportes con acceso publico luego de cada ejecucion.

#### Mantenimiento y buenas prácticas

- ~~Implementar limpieza automática de reportes antiguos de Allure.~~ Listo
- Añadir soporte para archivos `.env` y centralizar la configuración de variables.
