import tkinter as tk
from tkinter import messagebox

class MediaItem(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super(MediaItem, self).__init__(parent, *args, **kwargs)
        self.checked = tk.BooleanVar()

    def get_data(self):
        return {
            'id':self.id,
            'name': self.name, 
            'url': self.url, 
            'type': self.mtype,
            'duration': self.duration
        }

    def set_data(self, media):
        self.id = media['id']
        self.name = media['name']
        self.url = media['url']
        self.mtype = media['type']
        self.duration = int(media['duration']) if 'duration' in media else 0
        self.timepoint = int(media['timepoint']) if 'timepoint' in media else 0

    def deletemedia(self, evt):
        if messagebox.askyesno("PiepMe", "Are you sure to delete this resource?"):
            self.parentTab.deleteMediaItem([self.id])
            self.destroy()

            