import src.utils.kivyhelper as kv_helper
from src.utils import helper
from threading import Thread, Event
from kivy.clock import Clock, mainthread
from kivy.graphics import Fbo, ClearColor, ClearBuffers, Scale, Translate
from kivy.uix.relativelayout import RelativeLayout
from src.modules.kvcam.kivycameramain import KivyCameraMain
from src.modules.kvcam.kivycameramini import KivyCameraMini
from src.modules.custom.pieplabel import PiepLabel
from src.modules.custom.piepimage import PiepImage
from kivy.properties import ObjectProperty,NumericProperty
from kivy.lang import Builder
from src.models.normal_model import Normal_model
import subprocess, cv2, time, array, os, datetime
import numpy as np

Builder.load_file('src/ui/mainstream.kv')
class MainStream(RelativeLayout):
    camera= ObjectProperty()
    cameraMini= ObjectProperty()
    f_parent= ObjectProperty(None)
    typeSwitch = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MainStream, self).__init__(**kwargs)
        self.f_width = 1280
        self.f_height = 720
        self.capture = None
        self.fps = 25
        self.v_bitrate = "3072k"
        self.urlStream = ''
        self.devAudio = None
        self.deviceVolume = 100
        self.isStream = False
        self.isRecord = False
        self.pipe = None
        self.pipe2 = None
        self.lsSource = []
        self.command = []
        self.event = None
        self.canvas_parent_index = 0
        self.stop = Event()
        self.reconnect = 0
        self.streamType = ''
        self.mgrSchedule = None
        self.is_loop = True
        self.current_schedule = -1
        self.deleteAllFile()
        timenow = datetime.datetime.now().strftime("%d%m%y%H%M%S")
        self.url_flv = '../resource/temp/{}.flv'.format(timenow)
        self.url_flv_hls = '../resource/temp/{}_hls.flv'.format(timenow)
        self.mini_url_flv = '../resource/temp/mini_{}.flv'.format(timenow)
        self.mini_url_flv_hls = '../resource/temp/mini_{}_hls.flv'.format(timenow)
        del timenow

    def _load(self):
        try:
            command =  f'ffmpeg/ffmpeg.exe -y -nostats -loop 1 -i {helper._IMAGES_PATH}splash.jpg -i ../resource/media/muted.mp3 -filter_complex:0 "scale=-1:720,pad=1280:720:(1280-iw)/2:(720-ih)/2,setsar=1" -filter_complex:1 "volume=0" -r 25 {self.url_flv} {self.url_flv_hls} {self.mini_url_flv} {self.mini_url_flv_hls}'
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.pipe2 = subprocess.Popen(command, startupinfo=si)
            Clock.schedule_once(lambda x: self.pipe2.kill() , 5)
        except IOError:
            pass

    def show_camera_mini(self):
        self.cameraMini.opacity = 1

    def hide_camera_mini(self):
        if self.cameraMini.capture is not None:
            self.refresh_stream()
        self.cameraMini.opacity = 0
        self.cameraMini.release()

    def switch_display(self):
        try:
            self.remove_widget(self.camera)
            self.remove_widget(self.cameraMini)
            if self.typeSwitch == 0:
                self.typeSwitch =1
                self.camera.width = 320
                self.camera.height = 180
                self.cameraMini.width = 1280
                self.cameraMini.height = 720
                self.camera.pos = self.cameraMini.pos
                self.cameraMini.pos = (0,0)
                self.add_widget(self.cameraMini,1)
                self.add_widget(self.camera,1)
            elif self.typeSwitch == 1:
                self.typeSwitch = 0
                self.camera.width = 1280
                self.camera.height = 720
                self.cameraMini.width = 320
                self.cameraMini.height = 180
                self.cameraMini.pos = self.camera.pos
                self.camera.pos = (0,0)
                self.add_widget(self.camera,1)
                self.add_widget(self.cameraMini,1)
        except:
            pass
    
    def _set_capture(self, data_src, data_type, is_from_schedule):
        if self.mgrSchedule is not None:
            self.mgrSchedule.cancel()
        self.streamType = data_type
        self.camera.f_parent = self
        self.camera.set_data_source(data_src, data_type)
        self.f_parent.refresh_select_source(data_type)

    def _set_captureMini(self, data_src, data_type, is_from_schedule):
        self.cameraMini.f_parent = self
        self.cameraMini.set_data_source(data_src, data_type)

    def refresh_stream(self):
        if self.isStream is True:
            self.pipe.kill()
            self.prepare()

    def _set_source(self,lsSource):
        self.lsSource = lsSource

    def is_streaming(self):
        return self.isStream

    def record(self):
        if self.record:
            self.isRecord = False
        else:
            self.isRecord = True

    def startStream(self):
        try:
            if self.event is not None:
                self.event.cancel()
            self.fbo = Fbo(size=(self.f_width, self.f_height))
            with self.fbo:
                ClearColor(0, 0, 0, 1)
                ClearBuffers()
                Scale(1, -1, 1)
                Translate(-self.x, -self.y - self.f_height, 0)
            self.fbo.add(self.canvas)

            self.isStream = True
            # Thread(target=self._process).start()
            self._process()
        except IOError:
            kv_helper.getApRoot().triggerStop()
        

    def _process(self):
        self.event = Clock.schedule_interval(self.stream, 1/25)

    @mainthread
    def stream(self, fps):
        try:
            if self.isStream:
                # if self.parent is not None:
                #     self.canvas_parent_index = self.parent.canvas.indexof(self.canvas)
                #     if self.canvas_parent_index > -1:
                #         self.parent.canvas.remove(self.canvas)
                # self.fbo.add(self.canvas)
                self.fbo.draw()
                self.pipe.stdin.write(self.fbo.pixels)
                # self.fbo.remove(self.canvas)
                # if self.parent is not None and self.canvas_parent_index > -1:
                #     self.parent.canvas.insert(self.canvas_parent_index, self.canvas)
                self.reconnect = 0
        except:
            self.stopStream()
            self.reconnect += 2
            normal = Normal_model()
            key = self.f_parent.bottom_left.stream_key.text.split("?")[0]
            normal.reset_link_stream(key)
            Clock.schedule_once(self.reconnecting,self.reconnect)
            
    def reconnecting(self, dt):
        if self.reconnect > 10:
            kv_helper.getApRoot().triggerStop()
        else:
            if bool(self.prepare()):
                self.startStream()
    
    def stopStream(self):
        self.isStream = False
        if self.event is not None:
            self.event.cancel()
        if self.pipe is not None:
            self.pipe.kill()
        if self.stop is not None:
            self.stop.set()
        self.fbo.remove(self.canvas)
        # if self.parent is not None and self.canvas_parent_index > -1:
        #     self.parent.canvas.insert(self.canvas_parent_index, self.canvas)
        print("--- STOP ---")
        
    def set_url_stream(self, urlStream):
        self.urlStream = urlStream

    def set_device_audio(self, devAudio):
        self.devAudio = devAudio

    def draw_element(self):
        numau = 0
        inp = []
        txt = _map = ''

        numau += 1
        inp.extend(['-stream_loop','-1',"-i", '../resource/media/muted.mp3'])
        txt += f"[{numau}:a]volume=0[a{numau}];"
        _map += f'[a{numau}]'

        if self.camera.resource_type == "VIDEO" or self.camera.resource_type == "M3U8":
            url = self.url_flv
            if self.camera.resource_type == "M3U8":
                url = self.url_flv_hls
            numau += 1
            if self.camera.duration_current == 0:
                inp.extend(["-i", url])
            else:
                inp.extend(["-ss", helper.convertSecNoToHMS(self.camera.duration_current),"-i", url,"-flags","+global_header"])
            txt += f"[{numau}:a]volume=1[a{numau}];"
            _map += f'[a{numau}]'

        if self.f_parent.showMiniD is True:
            url = self.mini_url_flv
            if self.cameraMini.resource_type == "M3U8":
                url = self.mini_url_flv_hls
            numau += 1
            if self.cameraMini.duration_current == 0:
                inp.extend(["-i", url])
            else:
                inp.extend(["-ss", helper.convertSecNoToHMS(self.cameraMini.duration_current),"-i", url,"-flags","+global_header"])
            txt += f"[{numau}:a]volume=1[a{numau}];"
            _map += f'[a{numau}]'

        if 'audio' in self.camera.data_src:
            if self.camera.data_src['audio'] != '':
                inp.extend(['-stream_loop','-1',"-i", self.camera.data_src['audio']])
                numau += 1
                txt += f'[{numau}:a]volume=1[a{numau}];'
                _map += f'[a{numau}]'

        if len(self.lsSource) > 0:
            for value in self.lsSource:
                if value['active'] == 1:
                    if value['type'] == 'audio' and os.path.exists(value['src']) is True:
                        inp.extend(['-stream_loop','-1',"-i", value['src']])
                        numau += 1
                        txt += f'[{numau}:a]volume={str(value["volume"]/100)}[a{numau}];'
                        _map += f'[a{numau}]'
        if self.devAudio is not None:
            inp.extend(['-f', 'dshow', '-i', 'audio={}'.format(self.devAudio)])
            numau += 1
            txt += f"[{numau}:a]volume={str(self.deviceVolume/100)}[a{numau}];"
            _map += f'[a{numau}]'

        if numau > 0:
            txt += _map + f'amix={str(numau)}[a]'

        if len(txt) > 0:
            inp.extend(['-filter_complex', txt,'-map','0:v', '-map','[a]'])
            
        return inp

    def prepare(self):
        try:
            self.command = ['ffmpeg/ffmpeg.exe','-y','-framerate', '25','-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '{}x{}'.format(self.f_width, self.f_height), '-i', '-']
            
            self.command.extend(self.draw_element())
            # encode
            self.command.extend(['-vb', str(self.v_bitrate),'-r', '25', '-pix_fmt', 'yuv420p','-g','60'])

            self.command.extend(["-vf", "fps=25",'-metadata', 'title="PiepLiveCenter"'])
            # tream
            self.command.extend(['-f', 'flv', self.urlStream])
            
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.pipe = subprocess.Popen(self.command, stdin=subprocess.PIPE, startupinfo=si)
            return True

        except IOError:
            print("Exception prepare:")
            return False
            
    def prepare_audio(self):
        pass

    def release(self):
        try:
            if self.event is not None:
                self.event.cancel()
            if self.pipe is not None:
                self.pipe.kill()
            if self.camera is not None:
                self.camera.release()
            if self.pipe2 is not None:
                self.pipe2.kill()
            if self.mgrSchedule is not None:
                self.mgrSchedule.cancel()
            if os.path.exists(self.url_flv):
                os.remove(self.url_flv)
            if os.path.exists(self.url_flv_hls):
                os.remove(self.url_flv_hls)
            if os.path.exists(self.mini_url_flv):
                os.remove(self.mini_url_flv)
            if os.path.exists(self.mini_url_flv_hls):
                os.remove(self.mini_url_flv_hls)
        except IOError:
            print("Exception prepare:")
            return False

    def on_change_Volume(self, id, value):
        if id is not None and value is not None:
            if id != -1:
                for _s in self.lsSource:
                    if _s['id'] == id:
                        _s['volume'] = value
                        helper._write_lsStaticSource(self.lsSource)
                        break
            else:
                self.deviceVolume = value

            if self.isStream is True:
                self.pipe.kill()
                self.prepare()

    def on_change_position(self, id, pos_x, pos_y, parentName):
        self.f_parent.on_change_position(id, pos_x, pos_y)

    def show_text(self, id, text, font, size, color, pos_x, pos_y, active, new):
        if new:
            pText = PiepLabel(text='[color=' + str(color) + ']' + text + '[/color]',
                            font_size=size,
                            font_name=font,
                            x=pos_x,
                            y=pos_y,
                            markup=True,
                            opacity=active,
                            id=id,
                            parentName='main')
            self.add_widget(pText)
        else:
            for child in self.children:
                if child.id != None and child.id == id:
                    child.text = '[color=' + str(color) + ']' + text + '[/color]'
                    child.font_size = str(size)
                    child.font_name = font
                    #child.x = pos_x
                    #child.y = pos_y
                    #child.markup = True
                    #child.opacity = active
                    #child.idx = idx
                    break


    def show_image(self, id, src, pos_x, pos_y, w, h, active, new):
        if new:
            pimage = PiepImage(source=src,
                            size_hint=(None,None),
                            width=w,
                            height=h,
                            x=pos_x,
                            y=pos_y,
                            opacity=active,
                            id=id,
                            parentName='main')
            self.add_widget(pimage)
        else:
            for child in self.children:
                if child.id != None and child.id == id:
                    child.source = src
                    child.size = (w, h)
                    break

    def on_off_source(self, id, value):
        for child in self.children:
            if child.id != None and child.id == id:
                if value:
                    child.opacity = 1
                else:
                    child.opacity = 0
                break

    def on_change_audio(self):
        if self.isStream is True:
            self.pipe.kill()
            self.prepare()

    def start_schedule(self, isSchedule):
        if self.mgrSchedule is not None:
            self.mgrSchedule.cancel()
        self.ls_schedule = self.f_parent.right_content.tab_schedule.ls_schedule.get_data()

        if isSchedule:
            index = self.f_parent.right_content.tab_schedule.ls_schedule.getCurrentIndex()
            self.mgrSchedule = Clock.schedule_once(self.process_schedule , self.ls_schedule[index]['duration']+3)
    
    def process_schedule(self, fps):
        self.ls_schedule = self.f_parent.right_content.tab_schedule.ls_schedule.get_data()
        if self.mgrSchedule is not None:
            self.mgrSchedule.cancel()
        self.current_schedule = self.f_parent.right_content.tab_schedule.ls_schedule.getCurrentIndex() + 1
        if self.current_schedule >= len(self.ls_schedule):
            if self.is_loop:
                self.current_schedule = 0
            else:
                return False
        data_src = self.ls_schedule[self.current_schedule]
        self.f_parent.right_content.tab_schedule.ls_schedule.setPlayed(self.current_schedule)
        self._set_capture(data_src, 'SCHEDULE', True)

    def loop_schedule(self,_val):
        self.is_loop = _val
        
    def deleteAllFile(self):
        folder = '../resource/temp'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception:
                pass