from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import warnings
import string
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import StringProperty

Builder.load_string('''
<ScrolllabelLabel>:
    Label:
        text: root.text
        font_size: 50
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
''')


class ScrolllabelLabel(ScrollView):
    text = StringProperty('')


class SomeApp(App):
    def build(self):
        grid = GridLayout(cols=1, size_hint_x=None, width="600dp")

        # create a label instance
        self.lbl0 = Label(text='Tap and type a word/phrase below')
        grid.add_widget(self.lbl0)  # physically add the label onto the layout

        # create a text input instance
        self.txt1 = TextInput(text='', multiline=True)
        # physically add the text input onto the layout
        grid.add_widget(self.txt1)

        self.lbl1 = ScrolllabelLabel(text='Display')  # create a label instance
        grid.add_widget(self.lbl1)  # physically add the label onto the layout

        btn1 = Button(text='Press')  # create a button instance
        # binding the button with the function below
        btn1.bind(on_press=self.mirror)
        grid.add_widget(btn1)

        return grid

    def mirror(self, userInput):
        self.lbl1.text = self.txt1.text


SomeApp().run()
