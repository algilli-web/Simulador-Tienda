from app.vistas import VistaTituloPagina, VistaCatalogo
from app.modelos import DAO_SQLite_Producto, Tiquet
from simple_screen import cls, locate, Input, Screen_manager, DIMENSIONS

class SimuladorCaja:
    def __init__(self):
        self.tituloPagina = VistaTituloPagina("SIMULADOR DE CAJA")
        self.daoProductos = DAO_SQLite_Producto("data/productos.db")
        self.vista_catalogo = VistaCatalogo([], 0, 2, 10)
        self.tiquet = Tiquet({})

    def run(self):
        continuar = "S"
        with Screen_manager:
            while continuar.upper() == "S":
                cls()
                productos = self.daoProductos.todos()
                self.vista_catalogo.productos = productos
                self.vista_catalogo.tiquet = self.tiquet
                self.tituloPagina.paint()
                self.vista_catalogo.paint()

                codigo = self.vista_catalogo.get_codigo_producto()

                if codigo.upper() == "X":
                    self.mostrar_total()
                    continuar = Input("¿Nueva compra? (S/N): ")
                    if continuar.upper() == "S":
                        self.tiquet = Tiquet({})
                else:
                    producto = self.buscar_producto(codigo)
                    if producto:
                        unidades = self.pedir_unidades()
                        if unidades > 0:
                            self.tiquet.agregar_producto(producto, unidades)
                            self.mostrar_mensaje(f"Producto {producto.nombre} agregado al carrito.")
                        else:
                            self.mostrar_error("El número de unidades debe ser mayor que 0.")
                    else:
                        self.mostrar_error("Código de producto no existe.")
                    
                    Input("Presione Enter para continuar...")

    def buscar_producto(self, codigo):
        try:
            codigo = int(codigo)
            return next((p for p in self.vista_catalogo.productos if p.id == codigo), None)
        except ValueError:
            return None

    def pedir_unidades(self):
        try:
            locate(0, DIMENSIONS.h - 1, "Ingrese el número de unidades:")
            unidades = int(Input())
            return unidades
        except ValueError:
            return -1

    def mostrar_total(self):
        cls()
        print("Resumen de compra:")
        for producto_id, cantidad in self.tiquet.items.items():
            producto = self.buscar_producto(str(producto_id))
            if producto:
                subtotal = producto.precio_unitario * cantidad
                print(f"{producto.nombre}: {cantidad} unidades - {subtotal:.2f} €")
        print(f"Total: {self.tiquet.total:.2f} €")

    def mostrar_error(self, mensaje):
        locate(0, DIMENSIONS.h - 2, f"Error: {mensaje}")

    def mostrar_mensaje(self, mensaje):
        locate(0, DIMENSIONS.h - 2, mensaje)
        