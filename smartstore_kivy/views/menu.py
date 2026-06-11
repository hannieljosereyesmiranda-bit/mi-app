from kivy.uix.screenmanager import Screen
import database as db

class MenuScreen(Screen):
    def on_enter(self):
        productos = db.obtener_productos()
        stock_total = db.obtener_stock_total()
        self.ids.bienvenido.text = f"Bienvenido, {self.manager.usuario_actual['nombre']}"
        self.ids.total_productos.text = f"Total de productos: {len(productos)}"
        self.ids.stock_total.text = f"+ {stock_total}"