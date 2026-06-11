from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
import database as db
import webbrowser

class BuscarProductoScreen(Screen):
    def on_enter(self):
        tienda = db.obtener_tienda()
        nombre_tienda = tienda[1] if tienda else "Sin tienda"
        self.whatsapp = tienda[2] if tienda else None
        self.ids.tienda_label.text = f"Buscar Productos - {nombre_tienda}"
        self.buscar()

    def buscar(self):
        self.ids.resultados.clear_widgets()
        productos = db.obtener_productos_por_nombre(self.ids.buscar_input.text)
        if not productos:
            card = MDCard(size_hint_y=None, height=50, padding=10)
            card.add_widget(MDLabel(text="No se encontraron productos", halign="center"))
            self.ids.resultados.add_widget(card)
        else:
            for p in productos:
                card = MDCard(size_hint_y=None, height=150, padding=10, spacing=5)
                card.add_widget(MDLabel(text=p[1], font_style="H6"))
                card.add_widget(MDLabel(text=f"C${p[2]:.2f} / ${p[3]:.2f}", theme_text_color="Secondary"))
                card.add_widget(MDLabel(text=f"Stock: {p[4]}", theme_text_color="Hint"))
                btn_res = MDRaisedButton(text="Reservar", size_hint=(0.4, None), height=35)
                btn_res.bind(on_release=lambda x, pid=p[0], nom=p[1], s=p[4]: self.reservar(pid, nom, s))
                if self.whatsapp:
                    btn_wa = MDRaisedButton(text="📱 WhatsApp", size_hint=(0.4, None), height=35)
                    btn_wa.bind(on_release=lambda x: self.abrir_whatsapp())
                    row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
                    row.add_widget(btn_res)
                    row.add_widget(btn_wa)
                    card.add_widget(row)
                else:
                    card.add_widget(btn_res)
                self.ids.resultados.add_widget(card)

    def reservar(self, pid, nom, stock_act):
        if stock_act < 1:
            self.mostrar_error("Sin stock")
            return
        from kivy.uix.textinput import TextInput
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        cantidad_input = TextInput(text='1', multiline=False)
        content.add_widget(MDLabel(text=f"Reservar {nom}"))
        content.add_widget(cantidad_input)
        dialog = MDDialog(title="Cantidad", type="custom", content_cls=content, buttons=[
            MDFlatButton(text="Cancelar", on_release=lambda x: dialog.dismiss()),
            MDRaisedButton(text="Reservar", on_release=lambda x: self.confirmar_reserva(pid, nom, cantidad_input.text, stock_act, dialog))
        ])
        dialog.open()

    def confirmar_reserva(self, pid, nom, cantidad_str, stock_act, dialog):
        try:
            cant = int(cantidad_str)
            if 1 <= cant <= stock_act:
                db.agregar_reserva(self.manager.usuario_actual['id'], pid, cant)
                self.mostrar_error(f"{cant} x '{nom}' reservado")
                dialog.dismiss()
            else:
                self.mostrar_error("Cantidad inválida")
        except:
            self.mostrar_error("Cantidad inválida")

    def abrir_whatsapp(self):
        if self.whatsapp:
            numero = self.whatsapp.strip()
            if not numero.startswith("+"):
                numero = "+" + numero
            webbrowser.open(f"https://wa.me/{numero}")

    def mostrar_error(self, mensaje):
        dialog = MDDialog(text=mensaje, buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()