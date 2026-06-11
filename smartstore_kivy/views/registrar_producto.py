from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

class RegistrarProductoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_c = 0.0
        self.total_d = 0.0
        self.dialog = None

    def calcular(self):
        try:
            p = float(self.ids.precio.text)
            c = int(self.ids.stock.text)
            t = float(self.ids.tasa.text)
            n = self.ids.nombre.text
            if not n:
                self.mostrar_error("Ingrese nombre")
                return
            total_c = p * c
            total_d = total_c / t
            self.total_c += total_c
            self.total_d += total_d
            self.ids.resultado.text = f"{n}: C${total_c:.2f} / ${total_d:.2f}"
            self.ids.total_text.text = f"Total acumulado: C${self.total_c:.2f} / ${self.total_d:.2f}"
            self.ids.nombre.text = ""
            self.ids.precio.text = ""
            self.ids.stock.text = ""
        except:
            self.mostrar_error("Error en datos")

    def mostrar_error(self, mensaje):
        if not self.dialog:
            self.dialog = MDDialog(text=mensaje, buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
        else:
            self.dialog.text = mensaje
        self.dialog.open()