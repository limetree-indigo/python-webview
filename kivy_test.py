import kivy

import webview
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

# Window.size = (200, 200)
# Window.borderless = True

Window.maximize()


class MyApp(App):
    def button_click_callback(self, instance):
        window = webview.create_window("hands pos", 'http://pos.handsorder.com/')
        webview.start(gui="cef")

    def build(self):
        layout = BoxLayout(padding=10)
        button = Button(text='click', font_size=12)
        button.bind(on_press=self.button_click_callback)
        layout.add_widget(button)

        return layout

if __name__ == '__main__':
    MyApp().run()