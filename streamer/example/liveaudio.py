import subprocess
import cv2

# CAM SG - Vong Xoay Dien Bien Phu
# rtsp_link = 'rtsp://viewer:FB1D2631C12FE8F7EE8951663A8A108@14.241.245.161:554'

# cap = cv2.VideoCapture(rtsp_link)

# command = ['./ffmpeg',
#             '-thread_queue_size', '512',
#             '-r', '30',
#             '-f', 'rawvideo', 
#             '-pix_fmt', 'rgba',
#             '-s', '1280x720',
#             '-i','-',
#             '-re', '-i','output.wav',
#             '-b:a', '128k',
#             '-b:v', '1920k',
#             '-g', '30', '-r', '30',
#             '-threads', '2',
#             '-f','flv',
#             'rtmp://livevn.piepme.com/cam/7421.36d74d5063fda77f18871dbb6c0ce613?token=36d74d5063fda77f18871dbb6c0ce613&SRC=WEB&FO100=7421&PL300=8212&LN301=180&LV302=115.73.208.139&LV303=0982231325&LL348=1558771095036&UUID=247cbf2ee3f0bda1&NV124=vn&PN303=15&POS=3']
# pipe = subprocess.Popen(command, stdin=subprocess.PIPE)

# while True:
#     _, frame = cap.read()
#     pipe.stdin.write(frame)

# pipe.kill()
# cap.release()


######
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 50
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

command = ['./ffmpeg',
            '-f', 's16le',
            '-i','-',
            '-b:a', '128k',
            '-threads', '2',
            '-f','flv',
            '-y', 'recOut.flv']
pipe = subprocess.Popen(command, stdin=subprocess.PIPE)

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    # frames.append(data)
    pipe.stdin.write(data)

pipe.kill()

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()