# url para el online de parasoft
# BASE_URL = 'https://parabank.parasoft.com/parabank/services/bank'

# url para testear contra el clon en mi docker
# BASE_URL = 'http://localhost:8081/parabank/services/bank'

import os  # para usar la variable de entorno

BASE_URL = os.getenv("PARABANK_API_URL",
                     "http://localhost:8081/parabank/services/bank")
