from simple_screen import locate, DIMENSIONS, Input

class VistaTituloPagina:
    def __init__(self, texto: str, y: int = 0):
        self.texto = texto
        self.y = y

    def paint(self):
        x = (DIMENSIONS.w - len(self.texto)) // 2
        locate(x, self.y, self.texto)

class VistaCatalogo:
    def __init__(self, productos, x: int, y: int, num_filas: int, tiquet=None):
        self.productos = productos
        self.x = x
        self.y = y
        self.num_filas = num_filas
        self.tiquet = None

    def paint(self):
        max_filas = DIMENSIONS.h - self.y - 4
        filas_a_mostrar = min(len(self.productos), max_filas)

        locate(self.x, self.y, "Código | Producto  | Precio   | Unidades | Total")
        locate(self.x, self.y + 1, "-" * 50)

        for contador, producto in enumerate(self.productos[:filas_a_mostrar]):
            unidades = self.tiquet.obtener_cantidad(producto.id) if self.tiquet else 0
            total = producto.precio_unitario * unidades
            locate(self.x, self.y + 2 + contador, f"{producto.id:6d} | {producto.nombre:9s} | {producto.precio_unitario:6.2f} € | {unidades:8d} | {total:6.2f} €")

        if self.y + 2 + filas_a_mostrar + 1 < DIMENSIONS.h:
            locate(self.x, self.y + 2 + filas_a_mostrar + 1, "Ingrese el código del producto o 'X' para terminar:")
        else:
            locate(self.x, DIMENSIONS.h - 1, "Ingrese el código del producto o 'X' para terminar:")
    
    def get_codigo_producto(self):
        return Input()