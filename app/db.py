import sqlite3

try:
    mi_conexion = sqlite3.connect("instance/WCS.db")
    cursor = mi_conexion.cursor()

    # Tabla para ADMIS
    cursor.execute("""
        CREATE TABLE ADMIS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NUM_ID TEXT NOT NULL,
            NOMBRE TEXT,
            APELLIDO TEXT NOT NULL,
            USERNAME TEXT NOT NULL,
            CORREO TEXT,
            TELEFONO TEXT NOT NULL,
            CONTRASEÑA TEXT
        );
    """)

    # Tabla para MANEJADORES
    cursor.execute("""
        CREATE TABLE MANEJADORES (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE TEXT,
            APELLIDO TEXT NOT NULL,
            USERNAME TEXT NOT NULL,
            NUM_ID TEXT NOT NULL,
            CORREO TEXT,
            TELEFONO TEXT NOT NULL,
            CONTRASEÑA TEXT
        );
    """)

    # Tabla para PUNTOS_RECOLECCION
    cursor.execute("""
        CREATE TABLE PUNTOS_RECOLECCION (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_CAMIONES INTEGER,
            NOMBRE VARCHAR(50),
            UBICACION VARCHAR(100),
            CAPACIDAD INTEGER,
            ULTIMA_FECHA_RECOLECCION DATE,
            FOREIGN KEY (ID_CAMIONES) REFERENCES CAMIONES(ID)  
        );
    """)

    # Tabla para CAMIONES
    cursor.execute("""
        CREATE TABLE CAMIONES (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_MANEJADOR INTEGER NOT NULL,
            PLACA TEXT UNIQUE NOT NULL,  
            MODELO VARCHAR(50),
            CAPACIDAD INTEGER
        );
    """)

    # Tabla para Detalles
    cursor.execute("""
        CREATE TABLE DETALLES_RECOLECCION (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_MANEJADOR INTEGER,
            ID_CAMION INTEGER,
            ID_PUNTO_RECOLECCION INTEGER,  
            FECHA DATE NOT NULL,
            PLASTICO REAL NOT NULL,
            CARTON REAL NOT NULL,
            ORGANICOS REAL NOT NULL,
            FOREIGN KEY (ID_MANEJADOR) REFERENCES MANEJADORES(ID),
            FOREIGN KEY (ID_CAMION) REFERENCES CAMIONES(ID),
            FOREIGN KEY (ID_PUNTO_RECOLECCION) REFERENCES PUNTOS_RECOLECCION(ID) 
        );
    """)

    mi_conexion.commit()
    mi_conexion.close()

except Exception as ex:
    print(ex)
