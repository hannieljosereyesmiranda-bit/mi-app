from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
import database as db

class SmartStoreApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"
        db.inicializar_bd()
        
        sm = ScreenManager()
        sm.usuario_actual = None
        
        from views.pre_splash import PreSplashScreen
        from views.splash import SplashScreen
        from views.login import LoginScreen
        from views.menu import MenuScreen
        from views.registrar_producto import RegistrarProductoScreen
        from views.buscar_producto import BuscarProductoScreen
        from views.carrito import CarritoScreen
        from views.crear_tienda import CrearTiendaScreen
        from views.perfil import PerfilScreen
        
        sm.add_widget(PreSplashScreen(name='pre_splash'))
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(RegistrarProductoScreen(name='registrar_producto'))
        sm.add_widget(BuscarProductoScreen(name='buscar_producto'))
        sm.add_widget(CarritoScreen(name='carrito'))
        sm.add_widget(CrearTiendaScreen(name='crear_tienda'))
        sm.add_widget(PerfilScreen(name='perfil'))
        sm.current = 'pre_splash'
        return sm

if __name__ == '__main__':
    SmartStoreApp().run()