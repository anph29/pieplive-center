import cv2, subprocess
import numpy as np
#ffpyplayer for playing audio
from ffpyplayer.player import MediaPlayer


video_path="C:/Users/Thong/Desktop/piep-source/videos/anh-thuong-em-nhat-ma-30.mp4"
def PlayVideo(video_path):
    video=cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    while True:
        grabbed, frame=video.read()
        audio_frame, val = player.get_frame()
        if not grabbed:
            print("End of video")
            break
        if cv2.waitKey(28) & 0xFF == ord("q"):
            break
        cv2.imshow("Video", frame)
        if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame
    
    video.release()
    cv2.destroyAllWindows()

subprocess.Popen(PlayVideo(video_path))
