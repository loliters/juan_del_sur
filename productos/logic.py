#archivo temporal, clase que se usa para almacenar datos en memoria

class ProductoInMemoria:
    def __init__(self, id_prod, nombre, id_cat, p_compra, p_venta, estado, unidad, stock):
        self.id_producto = id_prod
        self.nom_producto = nombre
        self.id_categoria = id_cat
        self.precio_compra = float(p_compra)
        self.precio_venta = float(p_venta)
        self.estado = estado
        self.tipo_unidad = unidad
        self.stock_actual = int(stock)

    def calcular_ganancia(self):
        return self.precio_venta - self.precio_compra