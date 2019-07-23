from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty

Builder.load_string("""
<ToolTipLabel@Label>:
    size_hint: None, None
    size: self.texture_size[0]+10, self.texture_size[1]+10
    canvas.before:
        Color:
            rgb: 0.2, 0.2, 0.2
        Rectangle:
            size: self.size
            pos: self.pos
    markup:True
""")

class ImageButton(ButtonBehavior, Image):
    tooltip_text = StringProperty('')
    def __init__(self,  **kwargs):
        super(ImageButton, self).__init__()
        self.tooltip = Factory.ToolTipLabel(text='')#kwargs.get('tooltip_text')
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.open = False

    # def on_mouse_pos(self, *args):
    #     if not self.get_root_window():
    #         return

    #     pos = args[1]
    #     inside = self.collide_point(*self.to_widget(*pos))
    #     if inside and not self.open:
    #         self.tooltip.pos = pos
    #         self.display_tooltip()
    #         self.open = True
    #     elif not inside and self.open:
    #         #Clock.schedule_once(self.close_tooltip, .1)
    #         self.close_tooltip()
    #     elif inside and self.open:
    #         self.tooltip.pos = pos

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        self.tooltip.pos = pos
        Clock.unschedule(self.display_tooltip) # cancel scheduled event since I moved the cursor
        self.close_tooltip() # close if it's opened
        if self.collide_point(*self.to_widget(*pos)):
            Clock.schedule_once(self.display_tooltip, 0.5)

    def close_tooltip(self, *args):
        self.open = False
        Window.remove_widget(self.tooltip)

    def display_tooltip(self, *args):
        if self.tooltip_text != '':
            self.tooltip.text = self.tooltip_text
            Window.add_widget(self.tooltip)
