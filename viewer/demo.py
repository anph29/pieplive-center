from ffpyplayer.player import MediaPlayer
import time
import cv2

player = MediaPlayer("D:/RecordCam/out/phaohoa-chungket-anh.mp4")
val = ''
while val != 'eof':
    frame, val = player.get_frame()
    if val != 'eof' and frame is not None:
        img, t = frame
        # display img
        print(img, t)
