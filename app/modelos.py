import sqlite3
from abc import ABC, abstractmethod

class Model(ABC):
    @classmethod
    @abstractmethod
    def create_from_dict(cls, diccionario):
        pass

class Producto(Model):
    @classmethod
    def create_from_dict(cls, diccionario):
        return cls(diccionario["nombre"], float(diccionario["precio_unitario"]), int(diccionario["id"]))

    def __init__(self, nombre: str, precio_unitario: float, id: int = -1):
        self.nombre = nombre
        self.precio_unitario = precio_unitario
        self.id = id

    def __repr__(self):
        return f"Producto({self.id}): {self.nombre} - {self.precio_unitario:.2f}€"

    def __eq__(self, other):
        if isinstance(other, Producto):
            return self.nombre == other.nombre and self.precio_unitario == other.precio_unitario and self.id == other.id
        return False

    def __hash__(self):
        return hash((self.id, self.nombre, self.precio_unitario))

class Tiquet(Model):
    @classmethod
    def create_from_dict(cls, diccionario):
        return cls({
            int(diccionario["id_producto"]): int(diccionario["cantidad"])
        })

    def __init__(self, items: dict):
        self.items = items
        self.total = 0  # Se inicializa el total en 0

    def agregar_producto(self, producto, cantidad):
        if producto.id in self.items:
            self.items[producto.id] += cantidad
        else:
            self.items[producto.id] = cantidad
        self.total += producto.precio_unitario * cantidad

    def obtener_cantidad(self, id_producto):
        return self.items.get(id_producto, 0)

    def calcular_total(self, productos):
        self.total = sum(producto.precio_unitario * self.items[producto.id] 
                         for producto in productos if producto.id in self.items)

class DAO(ABC):
    @abstractmethod
    def todos(self):
        pass

    @abstractmethod
    def guardar(self, instancia):
        pass



class DAO_SQLite(DAO):
    model = None
    tabla = ""

    def __init__(self, path):
        self.path = path

    def todos(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {self.tabla}")
        nombres = list(map(lambda item: item[0], cur.description))
        resultado = self.__rows_to_dictlist(cur.fetchall(), nombres)
        conn.close()
        return resultado

    def __rows_to_dictlist(self, filas, nombres):
        registros = []
        for fila in filas:
            registro = {}
            for pos, nombre in enumerate(nombres):
                registro[nombre] = fila[pos]
            registros.append(self.model.create_from_dict(registro))
        return registros

    def guardar(self, instancia):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        campos = list(instancia.__dict__.keys())
        valores = list(instancia.__dict__.values())
        placeholders = ', '.join(['?' for _ in valores])
        cur.execute(f"INSERT INTO {self.tabla} ({', '.join(campos)}) VALUES ({placeholders})", valores)
        conn.commit()
        conn.close()

class DAO_SQLite_Producto(DAO_SQLite):
    model = Producto
    tabla = "productos"

class DAO_SQLite_Tiquet(DAO_SQLite):
    model = Tiquet
    tabla = "tiquets"