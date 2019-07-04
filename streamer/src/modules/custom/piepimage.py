from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.graphics import Rectangle, Color
from src.utils import kivyhelper
from kivy.clock import Clock
from kivy.lang import Builder
from functools import partial

kv = '''
<PiepImage>:
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 0
    keep_ratio: True
'''

Builder.load_string(kv)

class PiepImage(DragBehavior, Image):
    #callback = ObjectProperty(None)
    
    def __init__(self, idx, parentName, **kwargs):
        super(PiepImage, self).__init__(**kwargs)
        self.size_hint = None,None
        self.idx = idx
        self.parentName = parentName

    def on_touch_up(self, touch):
        if self._get_uid('svavoid') in touch.ud:
            return super(DragBehavior, self).on_touch_up(touch)

        if self._drag_touch and self in [x() for x in touch.grab_list]:
            touch.ungrab(self)
            self._drag_touch = None
            ud = touch.ud[self._get_uid()]
            if ud['mode'] == 'unknown':
                super(DragBehavior, self).on_touch_down(touch)
                Clock.schedule_once(partial(self._do_touch_up, touch), .1)
        else:
            if self._drag_touch is not touch:
                super(DragBehavior, self).on_touch_up(touch)
        if self.parentName != 'canvas':                
            kivyhelper.getApRoot().mainStream.on_change_position(self.idx,self.x,self.y, self.parentName)
        return self._get_uid() in touch.ud

    