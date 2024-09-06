import sqlite3
import csv

# Conectar a la base de datos (la creará si no existe)
conn = sqlite3.connect('data/productos.db')
cur = conn.cursor()

# Crear la tabla de productos
cur.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio_unitario REAL NOT NULL
)
''')

# Leer datos del archivo CSV e insertarlos en la base de datos
with open('data/productos.csv', 'r', encoding='utf-8') as f:
    csv_reader = csv.reader(f, delimiter=',')
    next(csv_reader)  # Saltar la fila de encabezados
    for row in csv_reader:
        cur.execute('INSERT INTO productos (id, nombre, precio_unitario) VALUES (?, ?, ?)',
                    (int(row[0]), row[1], float(row[2])))

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()