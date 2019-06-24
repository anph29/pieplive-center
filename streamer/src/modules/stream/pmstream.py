from src.modules.kvcam.kivycamera import KivyCamera
import kivy
import subprocess
import cv2
import numpy as np
import os
import src.utils.helper as helper
from kivy.core.window import Window

class PMStream(KivyCamera):

    def __init__(self, **kwargs):
        super(PMStream, self).__init__(**kwargs)
        self.capture = None
        self.f_width = 1280
        self.f_height = 720
        self.fps = 30
        self.v_bitrate = "50k"
        self.urlStream = ''
        self.devAudio = None
        self.deviceVolume = 100
        self.isStream = False
        self.pipe = None
        self.lsSource = []
        self.lsAudio = []
        self.command = []

    def changeCapture(self):
        # if self.isStream is True:
        #     self.pipe.kill()
        #     self.prepare()
        pass

    def is_streaming(self):
        return self.isStream

    #def processFrame(self, buffer):
        #self.__draw_label(buffer, 'PiepMe', (50, 1000), (0, 0, 0), (255, 255, 255), 3, cv2.FONT_HERSHEY_SIMPLEX)
        #self.__draw_image(buffer,'./images/mypicture.jpg')
        #return buffer

    def stream(self, bufferstring):
        try:
            if self.isStream is True:
                self.pipe.stdin.write(bufferstring.tostring())
        except IOError:
            #helper.getApRoot().triggerStop()
            pass

    def streamv2(self, bufferstring):
        try:
            self.pipe.stdin.write(bufferstring)
        except IOError:
            helper.getApRoot().triggerStop()

    def set_url_stream(self, urlStream):
        self.urlStream = urlStream

    def set_device_audio(self, devAudio):
        self.devAudio = devAudio
        #self.prepare()

    def add_text(self, name, label, posX, posY, font, size, color, shadowColor, shadowX, shadowY, box, boxColor, idx):
        text ={
            "type":"text",
            "active":1,
            "name": name,
            "label": label,
            "pos_x": posX,
            "pos_y": posY,
            "font": font,
            "size": size,
            "color": color,
            "shadow_color": shadowColor,
            "shadow_x": shadowX,
            "shadow_y": shadowY,
            "box": box,
            "box_color": boxColor,
            "idx": idx,
            'total':idx+1
        }
        self.lsSource.append(text)
        helper._write_lsStaticSource(self.lsSource)

    def add_image(self, name, src, posX, posY, width , height, timeStart, timeEnd, idx):
        image ={
            "type":"image",
            "active":1,
            "name": name,
            "src": src,
            "pos_x": posX,
            "pos_y": posY,
            "width": width,
            "height": height,
            "timeStart": timeStart,
            "timeEnd": timeEnd,
            "idx": idx,
            'total':idx+1
        }
        self.lsSource.append(image)
        helper._write_lsStaticSource(self.lsSource)

    def add_audio(self, name, src, volume, idx):
        num = self.lsSource[len(self.lsSource)-1]['total']
        audio = {
            "type":"audio",
            "active":1,
            "name":name,
            "src":src,
            "volume":volume,
            "idx": idx,
            'total':idx+1
        }
        self.lsSource.append(audio)
        helper._write_lsStaticSource(self.lsSource)
    
    def delete_source(self, index):
        del(self.lsSource[index])
        helper._write_lsStaticSource(self.lsSource)
    
    def draw_element(self):
        numau = 0
        inp = []
        txt = ''
        txt2 = ''
        if self.devAudio is not None:
            numau = 1
            txt2 +="volume={},".format(self.deviceVolume/100)
        if len(self.lsSource) > 0:
            for value in self.lsSource:
                if value['active'] == 1:
                    if(value['type'] == 'text'):
                        txt += "drawtext=text='{}':x={}:y={}:fontfile=src/fonts/{}.ttf:fontsize={}:fontcolor={}".format(value['label'], str(value['pos_x']), str(self.f_height - value['pos_y']), value['font'], str(value['size']), value['color'])
                        if value['shadow_color'] is not None:
                            txt += ":shadowcolor={}:shadowx={}:shadowy={}".format(value['shadow_color'], str(value['shadow_x']), str(value['shadow_y']))
                        if value['shadow_color'] is not None:
                            txt += ":box=1:boxcolor=black".format(str(value['box']), value['box_color'])
                        txt += ','
                
                    elif(value['type'] == 'image'):
                        inp.extend(["-i",value['src']])
                        txt += "overlay={}:{}".format(str(value['pos_x']), str(self.f_height - value['pos_y']))
                        if value['timeStart'] is not None and value['timeEnd'] is not None:
                            txt += ":enable='between(t,{},{})'".format(str(value['timeStart']), str(value['timeEnd']))
                        txt += ','

                    elif(value['type'] == 'audio'):
                        inp.extend(["-i",value['src']])
                        txt2 += 'volume={},'.format(str(value['volume']/100))
                        numau += 1
                
            if len(txt) > 0:
                txt = txt[:-1]
                inp.extend(['-filter_complex', txt])

            if numau > 0:
                txt2 += 'amix=inputs={}'.format(str(numau))
            if len(txt2) > 0:
                inp.extend(['-filter_complex:0', txt2])

        return inp

    def prepare(self):
        try:   
            if self.capture is None:
                return False
            self.command = ['ffmpeg-win/ffmpeg.exe', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '{}x{}'.format(self.f_width, self.f_height), '-i','-']
             #audio
            if self.devAudio is not None:
                self.command.extend(['-f','dshow','-i','audio={}'.format(self.devAudio),'-ar','44100', '-ac', '2', '-ab', '128'])
    
            self.command.extend(self.draw_element())
            #encode
            self.command.extend(['-vb', str(self.v_bitrate),'-framerate', '30', '-c:v', 'h264','-pix_fmt','yuv420p','-crf','23'])
            #tream
            self.command.extend(['-f', 'flv', self.urlStream])
            
            command = ['ffmpeg-win/ffmpeg.exe',
                '-f', 'rawvideo', 
                '-pix_fmt', 'rgba',#bgr24
                '-s', '1280x720',
                '-i','-',
                '-i','src/musics/anh-nang-trong-anh.mp3',
                '-vb','2500k',
                '-f','flv',
                '-s', '1280x720',
                'rtmp://livevn.piepme.com/cam/7421.b99e3cde588f1a8a25c0f002050f0893?token=b99e3cde588f1a8a25c0f002050f0893&SRC=WEB&FO100=7421&PL300=7939&LN301=180&LV302=115.73.208.139&LV303=0982231325&LL348=1554458516364&UUID=247cbf2ee3f0bda1&NV124=vn&PN303=15&POS=0']

            self.pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
            return True

        except IOError:
            return False
    
    def startStream(self):
        self.isStream = True
        print("--- START ---")

    def stopStream(self):
        self.isStream = False
        if self.pipe is not None:
            self.pipe.kill()
        print("--- STOP --a-")

    def release(self):
        if self.pipe is not None:
            self.pipe.kill()
        print("--- release ---")

    def __draw_label(self, buffer, text, pos, color, bg_color, scale, font_face):
        thickness = cv2.FILLED
        margin = 2
        txt_size = cv2.getTextSize(text, font_face, scale, thickness)
        end_x = pos[0] + txt_size[0][0] + margin
        end_y = pos[1] - txt_size[0][1] - margin

        #cv2.rectangle(buffer, pos, (end_x, end_y), bg_color, thickness)
        cv2.putText(buffer, text, pos, font_face, scale, color, 2, cv2.LINE_AA)

    def __draw_image(self, buffer, image):
        #img = cv2.imread(image,0)
        #cv2.imwrite(buffer,img)
        #line: buffer, start pos, end pos, color
        #cv2.line(buffer,(0,0),(150,150),(255,100,255),15)
        #cv2.rectangle(buffer,(105,205),(200,150),(0,0,255),-1)
        #cv2.circle(buffer,(100,63), 55, (0,255,0), -1)

        # pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
        # cv2.polylines(buffer, [pts], True, (0,255,255), 3)
     
        #cv2.Canny(buffer, 100, 200)
        #cv2.GaussianBlur(buffer, (1, 1), 0)

        #hsv = cv2.cvtColor(buffer, cv2.COLOR_BGR2HSV)
    
        #lower_red = np.array([30,150,50])
        #upper_red = np.array([255,255,180])
        
        #mask = cv2.inRange(hsv, lower_red, upper_red)
        #cv2.bitwise_and(buffer,buffer, mask= mask)

        #cv2.Laplacian(buffer,cv2.CV_64F)
        #cv2.Sobel(buffer,cv2.CV_64F,1,0,ksize=5)
        #cv2.Sobel(buffer,cv2.CV_64F,0,1,ksize=5)
        pass

        
    def on_touch_down(self, touch):
        # with self.canvas.before:
        #     Color(1, 0, 0)
        #     touch.ud["line"] = Line(points=(touch.x, touch.y), width=5)
        # return super(PMStream, self).on_touch_down(touch)
        pass

    def on_touch_move(self, touch):
        # touch.ud["line"].points += (touch.x, touch.y)
        # return super(PMStream, self).on_touch_move(touch)
        pass

    def on_off_source(self, index, value):
        if value is True:
            self.lsSource[index]["active"] = 1
        else:
            self.lsSource[index]["active"] = 0
        helper._write_lsStaticSource(self.lsSource)
        if self.isStream is True:
            self.pipe.kill()
            self.prepare()
    
    def on_change_Volume(self, idx, value):
        if idx is not None and value is not None:
            if idx != -1:
                for i, _s in enumerate(self.lsSource):
                    if _s['idx'] == idx:
                        _s['volume'] = value
                        helper._write_lsStaticSource(self.lsSource)
                        break
            else:
                self.deviceVolume = value
            if self.isStream is True:
                self.pipe.kill()
                self.prepare()

    def on_change_position(self, idx, pos_x, pos_y):
        for _s in self.lsSource:
            if _s['idx'] == idx:
                _s['pos_x'] = pos_x
                _s['pos_y'] = pos_y
                helper._write_lsStaticSource(self.lsSource)
                if self.isStream is True:
                    self.pipe.kill()
                    self.prepare()
                break
            