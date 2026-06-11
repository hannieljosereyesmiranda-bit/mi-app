from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import sqlite3
import database as db

class PerfilScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def on_enter(self):
        self.ids.nombre_label.text = f"Nombre: {self.manager.usuario_actual['nombre']}"
        self.ids.correo_label.text = f"Correo: {self.manager.usuario_actual['correo']}"

    def cambiar_pass(self):
        nueva = self.ids.nueva_pass.text
        confirma = self.ids.confirm_pass.text
        if not nueva or nueva != confirma:
            self.mostrar_error("Las contraseñas no coinciden")
            return
        conn = sqlite3.connect(db.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET contraseña = ? WHERE id = ?", (nueva, self.manager.usuario_actual['id']))
        conn.commit()
        conn.close()
        self.mostrar_error("Contraseña cambiada")
        self.ids.nueva_pass.text = ""
        self.ids.confirm_pass.text = ""

    def mostrar_error(self, mensaje):
        if not self.dialog:
            self.dialog = MDDialog(text=mensaje, buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
        else:
            self.dialog.text = mensaje
        self.dialog.open()