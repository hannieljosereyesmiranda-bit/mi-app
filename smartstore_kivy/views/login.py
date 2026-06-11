from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.app import MDApp
import database as db
from datetime import datetime

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.es_registro = False
        self.dialog = None

    def toggle(self):
        self.es_registro = not self.es_registro
        if self.es_registro:
            self.ids.titulo.text = "Crear Cuenta"
            self.ids.btn_accion.text = "Registrarse"
            self.ids.btn_alternar.text = "Volver a Iniciar Sesión"
            self.ids.nombre.opacity = 1
            self.ids.telefono.opacity = 1
            self.ids.fecha.opacity = 1
            self.ids.nombre.disabled = False
            self.ids.telefono.disabled = False
            self.ids.fecha.disabled = False
        else:
            self.ids.titulo.text = "Iniciar Sesión"
            self.ids.btn_accion.text = "Ingresar"
            self.ids.btn_alternar.text = "Crear cuenta nueva"
            self.ids.nombre.opacity = 0
            self.ids.telefono.opacity = 0
            self.ids.fecha.opacity = 0
            self.ids.nombre.disabled = True
            self.ids.telefono.disabled = True
            self.ids.fecha.disabled = True

    def accion(self):
        if self.es_registro:
            nombre = self.ids.nombre.text
            correo = self.ids.correo.text
            telefono = self.ids.telefono.text
            fecha = self.ids.fecha.text
            password = self.ids.password.text
            if not (nombre and correo and telefono and fecha and password):
                self.mostrar_error("Llena todos los campos")
                return
            try:
                edad = datetime.now().year - datetime.strptime(fecha, "%Y-%m-%d").year
                if edad < 17:
                    self.mostrar_error("Debes tener al menos 17 años")
                    return
            except:
                self.mostrar_error("Fecha inválida (YYYY-MM-DD)")
                return
            if db.registrar_usuario(nombre, correo, telefono, fecha, password):
                self.mostrar_error("Registro exitoso. Inicia sesión")
                self.toggle()
            else:
                self.mostrar_error("Correo ya existe")
        else:
            user = db.obtener_usuario(self.ids.correo.text, self.ids.password.text)
            if user:
                self.manager.usuario_actual = {"id": user[0], "nombre": user[1], "correo": user[2]}
                self.manager.current = 'menu'
            else:
                self.mostrar_error("Credenciales incorrectas")

    def mostrar_error(self, mensaje):
        if not self.dialog:
            self.dialog = MDDialog(text=mensaje, buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
        else:
            self.dialog.text = mensaje
        self.dialog.open()

    def recuperar(self):
        self.mostrar_error("Simulado: revisa tu correo")