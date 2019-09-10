import tkinter as tk
import vlc
from tkinter import messagebox
from src.utils import helper
from PIL import Image, ImageTk
from src.constants import UI
from src.enums import MediaType


class MediaItem(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MediaItem, self).__init__(parent, *args, **kwargs)
        self.checked = tk.BooleanVar()
        self.LN510 = 0
        self.id = None
        self.url = None
        self.rtpm = None
        self.name = None
        self.mtype = None
        self.audio = None
        self.audio_name = None
        self.duration = None
        self.timepoint = None
        self.audioPlayer = None
        self.playing_audio = False

    def get_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "type": self.mtype,
            "duration": self.duration,
            "timepoint": self.timepoint,
            "audio": self.audio,
            "audio_name": self.audio_name,
            "rtpm": self.rtpm,
        }

    def set_data(self, media):
        self.id = media["id"]
        self.name = media["name"]
        self.url = media["url"]
        self.mtype = media["type"]
        self.duration = int(media["duration"]) if "duration" in media else 0
        self.timepoint = int(media["timepoint"]) if "timepoint" in media else 0
        self.audio = media["audio"] if "audio" in media else ""
        self.audio_name = media["audio_name"] if "audio_name" in media else ""
        self.rtmp = media["rtmp"] if "rtmp" in media else ""

    def deleteMedia(self, evt):
        if self.parentTab.notWarningLocked() and messagebox.askyesno(
            "PiepMe", f"Are you sure to delete: `{self.name}`?"
        ):
            self.parentTab.deleteMediaItem([self.id])
            self.destroy()

    def updateLightColor(self, ln510):
        self.LN510 = ln510
        ## OFF
        frame = tk.PhotoImage(file=f"{helper._ICONS_PATH}live-red.png")
        if ln510 == 1:  # ON-WAITING
            frame = tk.PhotoImage(file=f"{helper._ICONS_PATH}live-orange.png")
        elif ln510 == 2:  # GOT-READY
            frame = tk.PhotoImage(file=f"{helper._ICONS_PATH}live-green.png")

        self.light.configure(image=frame)
        self.light.image = frame

    def activePresenter(self):
        self.stopGIF = False
        # count down 5 sec
        countFrame = [
            tk.PhotoImage(
                file=f"{helper._ICONS_PATH}count.gif", format=f"gif -index {i}"
            )
            for i in range(0, 15)
        ]

        def updateGIFCount(idx):
            if idx == 15:
                updateGIFLive(0)
            else:
                idx = (0, idx)[idx <= 14]
                frame = countFrame[idx]
                self.light.configure(image=frame)
                idx += 1
                if self.stopGIF:
                    self.updateLightColor(self.LN510)
                else:
                    if idx % 3 == 0:
                        timing = 700
                    elif idx % 3 == 1:
                        timing = 200
                    elif idx % 3 == 2:
                        timing = 100
                    #
                    self.after(timing, updateGIFCount, idx)

        # interval live stastus
        liveFrame = [
            tk.PhotoImage(
                file=f"{helper._ICONS_PATH}live.gif", format=f"gif -index {i}"
            )
            for i in range(0, 3)
        ]

        def updateGIFLive(idx):
            idx = (0, idx)[idx <= 2]
            frame = liveFrame[idx]
            self.light.configure(image=frame)
            idx += 1
            if self.stopGIF:
                self.updateLightColor(self.LN510)
            else:
                self.after(200, updateGIFLive, idx)

        # start point
        self.after(0, updateGIFCount, 0)

    def deactivePresenter(self):
        self.stopGIF = True

    def updatePlayIcon(self, ico):
        image = Image.open(f"{helper._ICONS_PATH}{ico}-b.png")
        imagetk = ImageTk.PhotoImage(image)
        self.lblPlay.configure(image=imagetk)
        self.lblPlay.image = imagetk

    def triggerStop(self):
        self.playing_audio = False
        self.audioPlayer.stop()
        self.updatePlayIcon("play-mp3")

    def playAudio(self, evt):
        if self.playing_audio:
            self.playing_audio = False
            self.audioPlayer.stop()
            self.updatePlayIcon("play-mp3")
        else:
            self.parentTab.stopAllAudio()
            self.audioPlayer = self.audioPlayer or vlc.MediaPlayer(self.audioSrc)
            self.playing_audio = True
            self.audioPlayer.play()
            self.updatePlayIcon("pause-mp3")
