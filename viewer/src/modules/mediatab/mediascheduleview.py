import tkinter as tk
from src.modules.custom import DDList
from . import MediaTab
from src.modules.mediaitem import MediaItemSchedule
from PIL import ImageTk, Image
from src.utils import helper
from src.modules.custom import VerticalScrolledFrame, ToolTip
from src.enums import MediaType
from src.modules.mediatab import MediaListView

class MediaScheduleView(MediaListView):
    def __init__(self, parent, *args, **kwargs):
        super(MediaScheduleView, self).__init__(parent, *args, **kwargs)

    def makeDDList(self, ref):
        return DDList(ref, 
            600,
            60,
            offset_x=5,
            offset_y=5,
            gap=5,
            item_borderwidth=1,
            item_relief=tk.FLAT,
            borderwidth=0,
            bg="#ccc")


    def addMediaToList(self, media):
        item = self.ddlist.create_item()
        medi = MediaItemSchedule(item, media=media)
        medi.pack(padx= (4,0), pady= (4,0), expand=True)
        self.ddlist.add_item(item)

