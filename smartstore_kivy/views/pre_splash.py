from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class PreSplashScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='😉', font_size='100sp', halign='center', valign='middle'))
        layout.add_widget(Label(text='SmartStore', font_size='32sp', bold=True, halign='center', valign='middle', color=(1,1,1,1)))
        self.add_widget(layout)
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'splash'), 10)