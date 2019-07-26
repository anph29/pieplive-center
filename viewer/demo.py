from tkinter import *
import time
import os
root = Tk()

frames = [PhotoImage(file='D:/anph/python/PiepLive-Center/resource/icons/sound.gif',format = 'gif -index %i' % i) for i in range(0, 5)]

def update(idx):
    idx = (0, idx)[idx <= 4]
    frame = frames[idx]
    idx += 1
    canvas.delete("all")
    canvas.create_image(20, 20, image=frame, anchor=NW)
    root.after(200, update, idx)

canvas = Canvas(root)
canvas.pack()
root.after(0, update, 0)
root.mainloop()