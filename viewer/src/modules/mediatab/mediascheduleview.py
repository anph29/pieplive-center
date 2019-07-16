import tkinter as tk
from src.modules.custom import DDList
from src.modules.mediaitem import MediaItemSchedule
from .medialistview import MediaListView

class MediaScheduleView(MediaListView):
    def __init__(self, parent, *args, **kwargs):
        super(MediaScheduleView, self).__init__(parent, *args, **kwargs)

    def makeDDList(self, ref):
        return DDList(ref, 
            600,
            50,
            offset_x=5,
            offset_y=5,
            gap=5,
            item_borderwidth=1,
            item_relief=tk.FLAT,
            borderwidth=0,
            bg="#ccc")


    def addMediaToList(self, media):
        item = self.ddlist.create_item()
        medi = MediaItemSchedule(item, parentTab=self, media=media)
        medi.pack(padx= (4,0), pady= (4,0), expand=True)
        self.ddlist.add_item(item)

