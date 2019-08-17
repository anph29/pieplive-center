from src.utils import helper, kivyhelper
from threading import Thread, Event
from kivy.clock import Clock
from kivy.graphics import Fbo, ClearColor, ClearBuffers, Scale, Translate, Canvas, Color, Rectangle
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
    _thread = None
    texture = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(MainStream, self).__init__(**kwargs)
        self.f_width = 1280
        self.f_height = 720

        # self.canvas = Canvas()
        # with self.canvas:
        #     self.fbo = Fbo(size=(self.f_width, self.f_height))
        #     self.fbo_color = Color(1, 1, 1, 1)
        #     self.fbo_rect = Rectangle()

        # with self.fbo:
        #     ClearColor(0, 0, 0, 0)
        #     ClearBuffers()
        #     # Scale(1, -1, 1)
        #     # Translate(-self.x, -self.y - self.f_height, 0)
        # self.texture = self.fbo.texture

        self.capture = None
        self.fps = 25
        self.v_bitrate = "4M"
        self.urlStream = ''
        self.devAudio = None
        self.deviceVolume = 100
        self.isStream = False
        self.isRecord = False
        self.pipe = None
        self.pipe2 = None
        self.command = []
        self.event = None
        self.canvas_parent_index = 0
        self.reconnect = 0
        self.streamType = ''
        self.mgrSchedule = None
        self.is_loop = True
        self.current_schedule = -1
        self.deleteAllFile()

    def _load(self):
        pass
    
    # def add_widget(self, *largs):
    #     canvas = self.canvas
    #     self.canvas = self.fbo
    #     ret = super(MainStream, self).add_widget(*largs)
    #     self.canvas = canvas
    #     return ret

    # def remove_widget(self, *largs):
    #     canvas = self.canvas
    #     self.canvas = self.fbo
    #     super(MainStream, self).remove_widget(*largs)
    #     self.canvas = canvas

    # def on_size(self, instance, value):
    #     self.fbo.size = value
    #     self.texture = self.fbo.texture
    #     self.fbo_rect.size = value

    # def on_pos(self, instance, value):
    #     self.fbo_rect.pos = value

    # def on_texture(self, instance, value):
    #     self.fbo_rect.texture = value

    def show_camera_mini(self):
        self.cameraMini.opacity = 1

    def hide_camera_mini(self):
        if self.cameraMini.capture is not None:
            self.refresh_stream()
        self.cameraMini.opacity = 0
        self.cameraMini.release()
        try:
            if self.typeSwitch == 1:
                self.remove_widget(self.camera)
                self.remove_widget(self.cameraMini) 
                self.typeSwitch = 0
                self.camera.width = 1280
                self.camera.height = 720
                self.cameraMini.width = 426#320
                self.cameraMini.height = 246#180
                self.cameraMini.pos = self.camera.pos
                self.camera.pos = (0,0)
                self.add_widget(self.cameraMini,0)
                self.add_widget(self.camera,1)
        except:
            pass

    def switch_display_auto(self):
        if self.cameraMini.opacity != 0:
            self.switch_display()

    def switch_display(self):
        try:
            self.remove_widget(self.camera)
            self.remove_widget(self.cameraMini)
            if self.typeSwitch == 0:
                self.typeSwitch =1
                self.camera.width = 426#320
                self.camera.height = 246#180
                self.cameraMini.width = 1280
                self.cameraMini.height = 720
                self.camera.pos = self.cameraMini.pos
                self.cameraMini.pos = (0,0)
                self.add_widget(self.camera,0)
                self.add_widget(self.cameraMini,1)
            elif self.typeSwitch == 1:
                self.typeSwitch = 0
                self.camera.width = 1280
                self.camera.height = 720
                self.cameraMini.width = 426#320
                self.cameraMini.height = 246#180
                self.cameraMini.pos = self.camera.pos
                self.camera.pos = (0,0)
                self.add_widget(self.cameraMini,0)
                self.add_widget(self.camera,1)
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
            self.camera.remove_file_flv()
            self.cameraMini.remove_file_flv()

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
            self._process()
        except IOError:
            kivyhelper.getApRoot().triggerStop()

    def _process(self):
        self.event = Clock.schedule_interval(self.stream, 1/25)
        self.f_parent.send_info_to_app()

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
            key = self.f_parent.streamKey.split("?")[0]
            normal.reset_link_stream(key)
            Clock.schedule_once(self.reconnecting,self.reconnect)
            
    def reconnecting(self, dt):
        if self.reconnect > 10:
            kivyhelper.getApRoot().triggerStop()
        else:
            if bool(self.prepare()):
                self.startStream()
    
    def stopStream(self):
        self.isStream = False
        if self.event is not None:
            self.event.cancel()
        if self.pipe is not None:
            self.pipe.kill()
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
        inp.extend(['-stream_loop','-1',"-i", helper._BASE_PATH+'media/muted.mp3'])
        txt += f"[{numau}:a]volume=0[a{numau}];"
        _map += f'[a{numau}]'

        if self.camera.resource_type == "VIDEO" or self.camera.resource_type == "MP4" or self.camera.resource_type == "M3U8":
            url = self.camera.url
            if os.path.exists(url):
                numau += 1
                if self.camera.duration_current == 0:
                    inp.extend(["-i", url])
                else:
                    inp.extend(["-ss", helper.convertSecNoToHMS(self.camera.duration_current),"-i", url,"-flags","+global_header"])
                txt += f"[{numau}:a]volume=1[a{numau}];"
                _map += f'[a{numau}]'

        if self.f_parent.showMiniD is True and (self.cameraMini.resource_type == "M3U8" or self.cameraMini.resource_type == "VIDEO" or self.cameraMini.resource_type == "MP4"):
            _url = self.cameraMini.url
            if os.path.exists(_url):
                numau += 1
                if self.cameraMini.duration_current == 0:
                    inp.extend(["-i", _url])
                else:
                    inp.extend(["-ss", helper.convertSecNoToHMS(self.cameraMini.duration_current),"-i", _url,"-flags","+global_header"])
                txt += f"[{numau}:a]volume=1[a{numau}];"
                _map += f'[a{numau}]'

        if 'audio' in self.camera.data_src and self.camera.data_src['audio'] != '':
            inp.extend(['-stream_loop','-1',"-i", self.camera.data_src['audio']])
            numau += 1
            txt += f'[{numau}:a]volume=1[a{numau}];'
            _map += f'[a{numau}]'

        
        lstAudio = self.f_parent.right_content.tab_audio.ls_audio.get_data() #helper._load_ls_audio()
        if len(lstAudio) > 0:
            for value in lstAudio:
                if value['active'] is True and os.path.exists(value['url']) is True:
                    inp.extend(['-stream_loop','-1',"-i", value['url']])
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
            self.command.extend(['-vb', str(self.v_bitrate),'-r', '25', '-pix_fmt', 'yuv420p'])

            self.command.extend(["-vf", "fps=25"])
            
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
            if self.cameraMini is not None:
                self.cameraMini.release()
            if self.pipe2 is not None:
                self.pipe2.kill()
            if self.mgrSchedule is not None:
                self.mgrSchedule.cancel()

            self.deleteAllFile()
            
        except IOError:
            print("Exception prepare:")
            return False

    def on_change_Volume(self, id, value):
        if id is not None and value is not None:
            if id != -1:
                pass
                # for _s in self.lsSource:
                #     if _s['id'] == id:
                #         _s['volume'] = value
                #         helper._write_lsStaticSource(self.lsSource)
                #         break
            else:
                self.deviceVolume = value

            if self.isStream is True:
                self.pipe.kill()
                self.prepare()

    def on_change_position(self, id, pos_x, pos_y, parentName):
        self.f_parent.on_change_position(id, pos_x, pos_y)

    def show_text(self, _id, text, font, size, color, pos_x, pos_y, active, new):
        if new:
            pText = PiepLabel(text='[color=' + str(color) + ']' + text + '[/color]',
                            font_size=size,
                            font_name=font,
                            x=pos_x,
                            y=pos_y,
                            markup=True,
                            opacity=active,
                            _id=_id,
                            parentName='main')
            self.add_widget(pText)
        else:
            for child in self.children:
                if child._id != None and child._id == _id:
                    child.text = '[color=' + str(color) + ']' + text + '[/color]'
                    child.font_size = str(size)
                    child.font_name = font
                    #child.x = pos_x
                    #child.y = pos_y
                    #child.markup = True
                    #child.opacity = active
                    #child.idx = idx
                    break


    def show_image(self, _id, src, pos_x, pos_y, w, h, active, new):
        if new:
            pimage = PiepImage(source=src,
                            size_hint=(None,None),
                            width=w,
                            height=h,
                            x=pos_x,
                            y=pos_y,
                            opacity=active,
                            _id=_id,
                            parentName='main')
            self.add_widget(pimage)
        else:
            for child in self.children:
                if child._id != None and child._id == _id:
                    child.source = src
                    child.size = (w, h)
                    break

    def on_off_source(self, _id, value):
        for child in self.children:
            if child._id != None and child._id == _id:
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
        folder = helper._BASE_PATH+'temp/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception:
                pass