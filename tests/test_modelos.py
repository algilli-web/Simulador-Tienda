from app.modelos import Producto, Tiquet

def test_create_producto():
    producto = Producto("Manzana", 0.5, 1)

    assert producto.nombre == "Manzana"
    assert producto.precio_unitario == 0.5
    assert producto.id == 1

def test_create_tiquet():
    tiquet = Tiquet({})

    assert tiquet.items == {}
    assert tiquet.total == 0

def test_agregar_producto_a_tiquet():
    tiquet = Tiquet({})
    producto = Producto("Manzana", 0.5, 1)

    tiquet.agregar_producto(producto, 3)

    assert tiquet.items == {1: 3}
    assert tiquet.total == 1.5

def test_obtener_cantidad_tiquet():
    tiquet = Tiquet({1: 3, 2: 5})

    assert tiquet.obtener_cantidad(1) == 3
    assert tiquet.obtener_cantidad(2) == 5
    assert tiquet.obtener_cantidad(3) == 0

def test_calcular_total_tiquet():
    tiquet = Tiquet({})
    productos = [
        Producto("Manzana", 0.5, 1),
        Producto("Plátano", 0.3, 2),
        Producto("Naranja", 0.7, 3)
    ]
    tiquet.agregar_producto(productos[0], 2)
    tiquet.agregar_producto(productos[1], 2)
    tiquet.agregar_producto(productos[2], 2)

    tiquet.calcular_total(productos)

    assert tiquet.total == 3