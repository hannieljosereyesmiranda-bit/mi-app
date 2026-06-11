from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
import database as db

class CrearTiendaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.productos_temp = []

    def on_enter(self):
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        main_layout.add_widget(Label(text='Crear Tienda', font_size=28, bold=True, size_hint_y=0.08, color=(4/255,4/255,74/255,1)))
        
        # ScrollView para todo el contenido
        scroll = MDScrollView(size_hint_y=0.85)
        content = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # ========== DATOS DE LA TIENDA ==========
        content.add_widget(Label(text='Datos de la tienda', font_size=20, bold=True, size_hint_y=None, height=30))
        
        self.nombre_input = MDTextField(hint_text='Nombre de la tienda', mode='round', size_hint_y=None, height=50)
        content.add_widget(self.nombre_input)
        
        self.whatsapp_input = MDTextField(hint_text='WhatsApp (ej: 50588888888)', mode='round', size_hint_y=None, height=50)
        content.add_widget(self.whatsapp_input)
        
        self.tasa_input = MDTextField(hint_text='Tasa de cambio (C$ por dólar)', text='36.5', mode='round', size_hint_y=None, height=50)
        content.add_widget(self.tasa_input)
        
        # Seguridad de la tienda (según el documento)
        content.add_widget(Label(text='Seguridad de la tienda', font_size=20, bold=True, size_hint_y=None, height=30))
        
        self.clave_input = MDTextField(hint_text='Contraseña para proteger la tienda', password=True, mode='round', size_hint_y=None, height=50)
        content.add_widget(self.clave_input)
        
        self.pregunta_input = MDTextField(hint_text='Pregunta de seguridad (ej: Nombre de tu mascota)', mode='round', size_hint_y=None, height=50)
        content.add_widget(self.pregunta_input)
        
        self.respuesta_input = MDTextField(hint_text='Respuesta a la pregunta de seguridad', mode='round', size_hint_y=None, height=50)
        content.add_widget(self.respuesta_input)
        
        # ========== REGISTRO DE PRODUCTOS ==========
        content.add_widget(Label(text='Registrar Productos', font_size=20, bold=True, size_hint_y=None, height=30))
        
        self.nombre_prod_input = MDTextField(hint_text='Nombre del producto', mode='round', size_hint_y=None, height=50)
        content.add_widget(self.nombre_prod_input)
        
        self.marca_input = MDTextField(hint_text='Marca (opcional)', mode='round', size_hint_y=None, height=50)
        content.add_widget(self.marca_input)
        
        self.talla_input = MDTextField(hint_text='Talla (opcional)', mode='round', size_hint_y=None, height=50)
        content.add_widget(self.talla_input)
        
        self.precio_input = MDTextField(hint_text='Precio en C$', mode='round', size_hint_y=None, height=50)
        content.add_widget(self.precio_input)
        
        self.cantidad_input = MDTextField(hint_text='Cantidad', mode='round', size_hint_y=None, height=50)
        content.add_widget(self.cantidad_input)
        
        # Botón para agregar producto
        btn_agregar = MDRaisedButton(text='Agregar Producto', size_hint_y=None, height=45, md_bg_color=(17/255,102/255,231/255,1))
        btn_agregar.bind(on_release=self.agregar_producto)
        content.add_widget(btn_agregar)
        
        # Lista de productos agregados
        content.add_widget(Label(text='Productos agregados:', font_size=16, bold=True, size_hint_y=None, height=30))
        self.productos_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.productos_layout.bind(minimum_height=self.productos_layout.setter('height'))
        content.add_widget(self.productos_layout)
        
        # Botón para guardar tienda
        btn_guardar = MDRaisedButton(text='Guardar Tienda', size_hint_y=None, height=50, md_bg_color=(239/255,165/255,32/255,1))
        btn_guardar.bind(on_release=self.guardar_tienda)
        content.add_widget(btn_guardar)
        
        # Botón para volver
        btn_volver = MDFlatButton(text='Volver al Menú', size_hint_y=None, height=40)
        btn_volver.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        content.add_widget(btn_volver)
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
        
        # Cargar datos si ya existe una tienda
        self.cargar_datos_tienda()

    def agregar_producto(self, instance):
        nombre = self.nombre_prod_input.text
        if not nombre:
            self.mostrar_error('Ingrese el nombre del producto')
            return
        try:
            precio = float(self.precio_input.text)
            cantidad = int(self.cantidad_input.text)
            tasa = float(self.tasa_input.text) if self.tasa_input.text else 36.5
        except:
            self.mostrar_error('Precio, cantidad y tasa deben ser números válidos')
            return
        
        marca = self.marca_input.text
        talla = self.talla_input.text
        precio_d = precio / tasa
        
        # Mostrar producto en la lista temporal
        card = MDCard(size_hint_y=None, height=60, padding=10, spacing=5, md_bg_color=(0.95,0.95,0.95,1))
        texto = f'{nombre}'
        if marca:
            texto += f' - {marca}'
        if talla:
            texto += f' - {talla}'
        texto += f' | C${precio:.2f} | x{cantidad} = C${precio*cantidad:.2f}'
        card.add_widget(Label(text=texto, size_hint_y=None, height=40))
        self.productos_layout.add_widget(card)
        self.productos_temp.append({'nombre': nombre, 'marca': marca, 'talla': talla, 'precio': precio, 'precio_d': precio_d, 'cantidad': cantidad})
        
        # Limpiar campos
        self.nombre_prod_input.text = ''
        self.marca_input.text = ''
        self.talla_input.text = ''
        self.precio_input.text = ''
        self.cantidad_input.text = ''
        
        self.mostrar_error(f'Producto "{nombre}" agregado')

    def guardar_tienda(self, instance):
        nombre = self.nombre_input.text.strip()
        if not nombre:
            self.mostrar_error('Ingrese el nombre de la tienda')
            return
        
        whatsapp = self.whatsapp_input.text.strip()
        try:
            tasa = float(self.tasa_input.text) if self.tasa_input.text else 36.5
        except:
            self.mostrar_error('Tasa de cambio inválida')
            return
        
        clave = self.clave_input.text
        pregunta = self.pregunta_input.text
        respuesta = self.respuesta_input.text
        
        # Guardar tienda en la base de datos
        db.guardar_tienda(nombre, whatsapp, clave, pregunta, respuesta, tasa)
        
        # Guardar los productos
        for prod in self.productos_temp:
            db.registrar_producto(prod['nombre'], prod['marca'], prod['talla'], prod['precio'], prod['precio_d'], prod['cantidad'])
        
        self.mostrar_error('Tienda y productos guardados correctamente')
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'menu'), 1.5)

    def cargar_datos_tienda(self):
        tienda = db.obtener_tienda()
        if tienda and len(tienda) >= 5:
            self.nombre_input.text = tienda[1] if tienda[1] else ''
            self.whatsapp_input.text = tienda[2] if tienda[2] else ''
            self.clave_input.text = tienda[3] if len(tienda) > 3 and tienda[3] else ''
            self.pregunta_input.text = tienda[4] if len(tienda) > 4 and tienda[4] else ''
            self.respuesta_input.text = tienda[5] if len(tienda) > 5 and tienda[5] else ''
            self.tasa_input.text = str(tienda[6]) if len(tienda) > 6 and tienda[6] else '36.5'
            # Cargar productos existentes
            self.cargar_productos_existentes()

    def cargar_productos_existentes(self):
        productos = db.obtener_productos()
        for p in productos:
            card = MDCard(size_hint_y=None, height=60, padding=10, spacing=5, md_bg_color=(0.95,0.95,0.95,1))
            texto = f'{p[1]} | C${p[2]:.2f} | x{p[4]}'
            card.add_widget(Label(text=texto, size_hint_y=None, height=40))
            self.productos_layout.add_widget(card)

    def mostrar_error(self, mensaje):
        if not self.dialog:
            self.dialog = MDDialog(text=mensaje, buttons=[MDFlatButton(text='OK', on_release=lambda x: self.dialog.dismiss())])
        else:
            self.dialog.text = mensaje
        self.dialog.open()