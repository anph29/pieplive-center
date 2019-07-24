import tkinter as tk
from tkinter import messagebox

class MediaItem(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super(MediaItem, self).__init__(parent, *args, **kwargs)
        self.checked = tk.BooleanVar()
        self.light = None
        self.id = None
        self.name = None
        self.url = None
        self.mtype = None
        self.duration = None
        self.timepoint = None
        self.audio = None
        self.rtpm = None
        
    def get_data(self):
        return {
            'id':self.id,
            'name': self.name, 
            'url': self.url, 
            'type': self.mtype,
            'duration': self.duration,
            'timepoint': self.timepoint,
            'audio':self.audio,
            'rtpm':self.rtpm
        }

    def set_data(self, media):
        self.id = media['id']
        self.name = media['name']
        self.url = media['url']
        self.mtype = media['type']
        self.duration = int(media['duration']) if 'duration' in media else 0
        self.timepoint = int(media['timepoint']) if 'timepoint' in media else 0
        self.audio = media['audio'] if 'audio' in media else ''
        self.rtmp = media['rtmp'] if 'rtmp' in media else ''

    def deleteMedia(self, evt):
        if messagebox.askyesno("PiepMe", "Are you sure to delete this resource?"):
            self.parentTab.deleteMediaItem([self.id])
            self.destroy()

    def updateLightColor(self, ln510):
        self.light.delete("all")
        self.LN510 = ln510
        color = "#F00" # 0: OFF
        if ln510 == 1: # Press ON
            color = "#FF0"
        elif ln510 == 2: # READY
            color = "#0F0"
        self.light.create_circle(6, 6, 6, fill=color, width=0)

