# este diccionario de diccionarios es el "esqueleto" que tiene que conicidir con la respuesta
schema_customer = {
    "id":         {"type": "integer"},
    "firstName":  {"type": "string"},
    "lastName":   {"type": "string"},
    "address": {
        "type": "dict",
        "schema": {
            "street":  {"type": "string"},
            "city":    {"type": "string"},
            "state":   {"type": "string"},
            "zipCode": {"type": "string"}
        }
    },
    "phoneNumber": {"type": "string"},
    "ssn":         {"type": "string"}
}
