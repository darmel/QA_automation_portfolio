import jaydebeapi

# ruta al .jar
hsqldb_jar = "./java-lib/hsqldb-jdk8.jar"

# conexion
conn = jaydebeapi.connect(
    "org.hsqldb.jdbcDriver",
    "jdbc:hsqldb:hsql://localhost:9001/parabank",
    ["sa", ""],
    hsqldb_jar
)

# crear cursor y ejecutar cosnulta
cursor = conn.cursor()
cursor.execute("SELECT * FROM CUSTOMER")

# mostrar resultado
for row in cursor.fetchall():
    print(row)

# cerrar conexion
cursor.close()
conn.close()
