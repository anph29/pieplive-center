import vlc
import tkinter as tk
from src.modules.custom import PLabel
import PIL
from PIL import Image, ImageTk
from PIL import BmpImagePlugin,GifImagePlugin,Jpeg2KImagePlugin,JpegImagePlugin,PngImagePlugin,TiffImagePlugin,WmfImagePlugin # to fuck -> OSerror: cannot identify image file
from src.utils import helper
from src.constants import UI
from .mediaitem import MediaItem
from src.modules.custom import ToolTip, CanvasC
import io
from src.enums import MediaType

Image._initialized = 2

class MediaItemBox(MediaItem):
    finished = False
    cell_width = 240
    top_height = 135
    bot_height = 25
    buffer = None
    zoomIn = False
    vlcInited = False
    def __init__(self, parent, parentTab=None, media=None, *args, **kwargs):
        super(MediaItemBox, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parentTab = parentTab
        self.set_data(media)
        self.botBg = '#BDC3C7'
        self.after(100, self.initGUI)

    def initGUI(self):
        ww = self.cell_width + 5
        wh = 5 + self.top_height + self.bot_height
        self.wrapper = tk.Frame(self, relief=tk.FLAT, bd=1 ,bg="#fff", width=ww, height=wh)
        self.wrapper.pack(expand=True)
        self.initTOP()
        self.initBOTTOM()
        if self.mtype == 'VIDEO':
            self.buffer = tk.Frame(self.wrapper, bd=0, relief=tk.SUNKEN, bg='#f00', width=0, height=3)
            self.buffer.pack(side=tk.LEFT, fill=tk.Y)

    def initTOP(self):
        self.top = tk.Frame(self.wrapper, bd=0, relief=tk.FLAT, bg="#ccc", width=self.cell_width, height=self.top_height)
        self.top.pack(side=tk.TOP)
        self.top.bind("<Button-1>", self.playOrPauseClick)
        if self.mtype == 'IMG':
            try:
                im = Image.open(self.url)
            except FileNotFoundError:
                im = Image.open(helper._IMAGES_PATH + 'splash.png')
        else:
            im = Image.open(helper._IMAGES_PATH + 'splash-video.png')
        w, h = im.size
        r = w / h   
        nH = self.top_height
        nW = int(nH * r)
        #   
        resized = im.resize((nW, nH), Image.ANTIALIAS)
        imgMedia = ImageTk.PhotoImage(resized)
        lblMedia = tk.Label(self.top, image=imgMedia, bg="#f2f2f2", cursor='hand2')
        lblMedia.photo = imgMedia
        #
        if self.mtype != 'IMG':
            lblMedia.bind('<Button-1>', self.initVLC)
        lblMedia.pack()

    def initBOTTOM(self):
        bottom = tk.Frame(self.wrapper, bd=5, relief=tk.FLAT, bg=self.botBg, width=self.cell_width, height=self.bot_height)
        bottom.pack(side=tk.BOTTOM, fill=tk.X)
        # traffic light
        if self.parentTab.tabType == MediaType.PRESENTER:
            self.light = CanvasC(bottom, width=15, height=15, borderwidth=0, highlightthickness=0, bg=self.botBg)
            self.light.pack(side=tk.LEFT)
            self.light.create_circle(6, 6, 6, fill="#F00", width=0)
        self.checkbox = tk.Checkbutton(bottom, variable=self.checked, onvalue=True, bg=self.botBg, offvalue=False, height=1, width=1, bd=0, relief=tk.FLAT)
        self.checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        # play
        if self.parentTab.tabType != MediaType.IMAGE:
            imagePlay = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}play-b.png"))
            self.lblPlay = tk.Label(bottom, image=imagePlay, bg=self.botBg, cursor='hand2')
            self.lblPlay.image = imagePlay
            self.lblPlay.bind("<Button-1>", self.playOrPauseClick)
            self.lblPlay.pack(side=tk.LEFT)
        # label
        lbl_name = PLabel(bottom, text=self.name, justify=tk.LEFT, elipsis=22, bg=self.botBg, font=UI.TXT_FONT, fg="#000")
        lbl_name.pack(side=tk.LEFT)
        # bin
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}trash-b.png"))
        lbl_trash = tk.Label(bottom, image=imageBin, bg=self.botBg, cursor='hand2')
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.deleteMedia)
        ToolTip(lbl_trash, "Delete") 
        lbl_trash.pack(side=tk.RIGHT)
        bottom.pack(side=tk.BOTTOM, fill=tk.X)
        # zoom
        imgZom = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}zoom-in.png"))
        self.lblZoom = tk.Label(bottom, image=imgZom, bg=self.botBg, cursor='hand2')
        self.lblZoom.image = imgZom
        self.lblZoom.bind("<Button-1>", self.toggleZoom) 
        self.lblZoom.pack(side=tk.RIGHT)
        ToolTip(self.lblZoom, "Zoom in")

    def initVLC(self, evt):
        if self.parentTab.tabType != MediaType.PRESENTER or (self.parentTab.tabType == MediaType.PRESENTER and self.LN510 == 2):
            self.Instance = vlc.Instance()
            self.player = self.Instance.media_player_new()
            self.player.audio_set_volume(0)
            self.initPlayerMedia()
            self.player.set_hwnd(self.top.winfo_id())
            self.play()
            if self.mtype == 'VIDEO':
                self.after(100, self.playOrPause)
            if self.mtype == 'RTSP':
                self.after(5000, self.playOrPause)
            self.vlcInited = True

    def toggleZoom(self, evt):
        w = self.winfo_width()
        h = self.winfo_height()
        x = self.winfo_x()
        y =  self.winfo_y()
        if self.zoomIn:
            # self.configure("geometry",f"{w*2}x{h*2}+{x}+{y}")
            self.updateZoomIcon('in')
            ToolTip(self.lblZoom, "Zoom in")
            self.zoomIn = False
        else:
            # self.configure("geometry",f"{w/2}x{h/2}+{x}+{y}")
            self.updateZoomIcon('out')
            ToolTip(self.lblZoom, "Zoom out")
            self.zoomIn = True

    def initPlayerMedia(self):
        self.media = self.Instance.media_new(self.url)
        self.player.set_media(self.media)
        self.media.release()

    def updateProgress(self):
        events = self.player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.on_end)
        nwidth = 0 if 0 == self.media.get_duration() else self.player.get_time() / self.media.get_duration() * self.cell_width
        self.buffer.config(width=nwidth)
        if self.finished:
            self.buffer.configure(width=self.cell_width)
        elif self.player.is_playing():
            self.after(1000, self.updateProgress)

    def on_end(self, evt):
        self.finished = True
        self.updatePlayIcon('f5')

    def play(self):
        if self.mtype == 'VIDEO':
            if self.finished:
                self.buffer.configure(width=0)
                self.player.stop()
                self.finished = False
            #
            self.after(1000,  self.updateProgress)
        self.player.play()

    def playOrPauseClick(self, _):
        self.playOrPause()

    def playOrPause(self):
        if self.parentTab.tabType != MediaType.PRESENTER or (self.parentTab.tabType == MediaType.PRESENTER and self.LN510 == 2):
            if not self.vlcInited:
                self.initVLC(None)
            if self.player.is_playing():
                self.player.pause()
                self.updatePlayIcon('play')
            else:
                self.play()
                self.updatePlayIcon('pause')

    def updatePlayIcon(self, ico):
        image = Image.open(f"{helper._ICONS_PATH}{ico}-b.png")
        imagetk = ImageTk.PhotoImage(image)
        self.lblPlay.configure(image=imagetk)
        self.lblPlay.image = imagetk

    def updateZoomIcon(self, ico):
        image = Image.open(f"{helper._ICONS_PATH}zoom-{ico}.png")
        imagetk = ImageTk.PhotoImage(image)
        self.lblZoom.configure(image=imagetk)
        self.lblZoom.image = imagetk

     def updateLightColor(self, ln510):
        super(MediaItemBox, self).updateLightColord(ln510)
        self.lblPlay.config(cursor='none')
        if ln510 == 1: # Press ON
            self.lblPlay.config(cursor="wait")
        elif ln510 == 2: # READY
            self.lblPlay.config(cursor='hand2')

