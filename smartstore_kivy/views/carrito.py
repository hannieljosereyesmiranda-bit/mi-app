from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import database as db

class CarritoScreen(Screen):
    def on_enter(self):
        self.cargar()

    def cargar(self):
        self.ids.lista.clear_widgets()
        reservas = db.obtener_reservas_usuario(self.manager.usuario_actual['id'])
        total_c = 0
        total_d = 0
        for r in reservas:
            rid, nom, cant, pc, pd, estado = r
            subtotal_c = pc * cant
            subtotal_d = pd * cant
            if estado == "Reservado":
                total_c += subtotal_c
                total_d += subtotal_d
            card = MDCard(size_hint_y=None, height=120, padding=10, spacing=5)
            card.add_widget(MDLabel(text=f"{nom} x{cant}", font_style="H6"))
            card.add_widget(MDLabel(text=f"C${pc:.2f} c/u = C${subtotal_c:.2f} / ${subtotal_d:.2f}", theme_text_color="Secondary"))
            card.add_widget(MDLabel(text=f"Estado: {estado}", theme_text_color="Hint"))
            if estado == "Reservado":
                row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
                btn_conf = MDRaisedButton(text="Confirmar", size_hint=(0.4, None), height=35)
                btn_conf.bind(on_release=lambda x, rid=rid: self.confirmar(rid))
                btn_can = MDRaisedButton(text="Cancelar", size_hint=(0.4, None), height=35)
                btn_can.bind(on_release=lambda x, rid=rid: self.cancelar(rid))
                row.add_widget(btn_conf)
                row.add_widget(btn_can)
                card.add_widget(row)
            self.ids.lista.add_widget(card)
        self.ids.total_text.text = f"Total: C${total_c:.2f} / ${total_d:.2f}"

    def confirmar(self, rid):
        db.confirmar_reserva(rid)
        self.cargar()

    def cancelar(self, rid):
        db.eliminar_reserva(rid)
        self.cargar()

    def confirmar_todo(self):
        reservas = db.obtener_reservas_usuario(self.manager.usuario_actual['id'])
        for r in reservas:
            if r[5] == "Reservado":
                db.confirmar_reserva(r[0])
        self.cargar()