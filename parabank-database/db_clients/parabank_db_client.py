"""Conexion a la base de datos
    Si hubiera más de una base de datos terndria que repetir esto"""


import jaydebeapi
import os
import pathlib

JAR_PATH = pathlib.Path(__file__).resolve(
).parent.parent / "java-lib" / "hsqldb-jdk8.jar"
URL = "jdbc:hsqldb:hsql://localhost:9001/parabank"
USER = "sa"
PWD = ""


def open_parabank_conn():
    return jaydebeapi.connect("org.hsqldb.jdbcDriver", URL, [USER, PWD], str(JAR_PATH))
