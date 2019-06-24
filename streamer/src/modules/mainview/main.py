from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from src.modules.bottomleft.controllers.bottomleft import TextDialog
from src.modules.bottomleft.controllers.bottomleft import ImageDialog
from src.modules.bottomleft.controllers.bottomleft import AudioDialog
from src.modules.login.login import Login
from src.modules.stream.mainstream import MainStream
from src.utils import helper
from kivy.lang import Builder
import sounddevice as sd
from threading import Thread, Event, ThreadError

Builder.load_file('src/modules/mainview/views/main.kv')


class MainView(Widget):
    mainStream = ObjectProperty()
    bottom_left = ObjectProperty()
    control = ObjectProperty()
    login_popup = ObjectProperty()
    right_content = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.lsAudio = []
        self.lsSource = []
        self.f_width = 1280
        self.f_height = 720
    
    def on_start(self):
        self.mainStream.f_parent = self
        setting = helper._read_setting()
        if setting['ouput_resolution'] is not None:
            self.f_width = self.mainStream.f_width = setting['ouput_resolution'][0]
            self.f_height = self.mainStream.f_height = setting['ouput_resolution'][1]
        if setting['vbitrate'] is not None:
            self.v_bitrate = self.mainStream.v_bitrate = setting['vbitrate']
        if setting['stream_server'] is not None:
            self.bottom_left.stream_server.text = setting['stream_server']
        if setting['stream_key'] is not None:
            self.bottom_left.stream_key.text = setting['stream_key']

        self.mainStream.urlStream = self.bottom_left.stream_server.text + \
            self.bottom_left.stream_key.text
        self.initAudio()
        self.initSource()
        self.init_right_content_cam()
        self.init_right_content_presenter()

    def init_right_content_cam(self):
        self.right_content.tab_camera.ls_camera.set_data()

    def init_right_content_presenter(self):
        self.right_content.tab_presenter.ls_presenter.set_data()

    def initAudio(self):
        self.audios = sd.query_devices(kind='input')
        if self.audios is not None:
            if 'Realtek High Defini' in self.audios['name']:
                self.audios['name'] += 'tion Audio)'
            _audio = {
                'name': self.audios['name'],
                'value': self.audios['name'],
                'volume': 100,
                'idx': -1
            }
            self.lsAudio.append(_audio)
            self.changeAudio(self.audios['name'])
            self.bottom_left.list_mixer.set_source(self.lsAudio)

    def initSource(self):
        self.lsSource = helper._load_lsStaticSource()
        self.mainStream.lsSource = self.lsSource
        self.bottom_left.list_source.set_source(self.lsSource)
        for idx, _s in enumerate(self.lsSource):
            _s['idx'] = idx
            _s['total'] = len(self.lsSource)
            # if _s['active'] == 1:
            if _s['type'] == 'text':
                self.mainStream.show_text(_s['label'], _s['font'], _s['size'],
                                          _s['color'], _s['pos_x'], _s['pos_y'], _s['active'], idx)
            elif _s['type'] == 'image':
                self.mainStream.show_image(_s['src'], _s['pos_x'], _s['pos_y'],
                                           _s['width'], _s['height'], _s['active'], idx)

    def changeSrc(self, data_src):
        if bool(data_src) and self.mainStream is not None:
            self.mainStream._set_capture(data_src)

    def changeAudio(self, value):
        if value is not None and self.mainStream is not None:
            self.mainStream.set_device_audio(value)

    def changeAudioVolume(self, idx, volume):
        if self.mainStream is not None:
            self.mainStream.on_change_Volume(idx, volume)

    def mClick(self, obj):
        if obj == 'start':
            if self.mainStream.isStream is False:
                if len(self.bottom_left.stream_server.text) == 0 or len(
                        self.bottom_left.stream_key.text) == 0:
                    return False
                self.mainStream.set_url_stream(
                    self.bottom_left.stream_server.text +
                    self.bottom_left.stream_key.text)
                if bool(self.mainStream.prepare()):
                    self.mainStream.startStream()
                    self.control.btn_start.text = "Stop Streaming"
                    self.control.btn_start.background_color = .29, .41, .15, 0.9

            elif self.mainStream.isStream is True:
                self.mainStream.stopStream()
                self.control.btn_start.text = "Start Streaming"
                self.control.btn_start.background_color = .29, .41, .55, 1

    def triggerStop(self):
        self.mainStream.stopStream()
        self.control.btn_start.text = "Start Streaming"
        self.control.btn_start.background_color = .29, .41, .55, 1

    def on_off_source(self, index, value):
        ite = self.lsSource[index]
        if ite['type'] == 'audio':
            if value:
                _audio = {'name':  ite['name'], 'value': ite['name'],
                          'volume': ite['volume'], 'idx': ite['idx']}
                self.bottom_left.list_mixer.add_source(_audio)
            else:
                self.bottom_left.list_mixer.del_source(ite['idx'])
        else:
            self.mainStream.on_off_source(ite['idx'], value)

        if value is True:
            self.lsSource[index]["active"] = 1
        else:
            self.lsSource[index]["active"] = 0

        helper._write_lsStaticSource(self.lsSource)

    def openSetting(self):
        pass

    def add_source(self, type):
        if type == 'IMAGE':
            obj = ImageDialog(self)
            obj.open()
        elif type == 'TEXT':
            obj = TextDialog(self)
            obj.open()
        elif type == 'AUDIO':
            obj = AudioDialog(self)
            obj.open()

    def add_text(self, name, label, font, size, color, pos_x, pos_y):
        idx = self.lsSource[len(self.lsSource)-1]['total']
        text = {
            "type": "text",
            "active": 1,
            "name": name,
            "label": label,
            "pos_x": pos_x,
            "pos_y": pos_y,
            "font": font,
            "size": size,
            "color": color,
            "shadow_color": None,
            "shadow_x": 0,
            "shadow_y": 0,
            "box": None,
            "box_color": None,
            "idx": idx,
            'total': idx+1
        }
        self.lsSource.append(text)
        helper._write_lsStaticSource(self.lsSource)
        self.mainStream.show_text(
            label, font, size, color, pos_x, pos_y, 1, idx)

    def add_image(self, name, src, pos_x, pos_y, width, height):
        idx = self.lsSource[len(self.lsSource)-1]['total']
        image = {
            "type": "image",
            "active": 1,
            "name": name,
            "src": src,
            "pos_x": pos_x,
            "pos_y": pos_y,
            "width": width,
            "height": height,
            "timeStart": None,
            "timeEnd": None,
            "idx": idx,
            'total': idx+1
        }
        self.lsSource.append(image)
        helper._write_lsStaticSource(self.lsSource)
        self.mainStream.show_image(src, pos_x, pos_y, width, height, 1, idx)

    def add_audio(self, name, src, volume):
        idx = self.lsSource[len(self.lsSource)-1]['total']
        audio = {
            "type": "audio",
            "active": 1,
            "name": name,
            "src": src,
            "volume": volume,
            "idx": idx,
            'total': idx+1
        }
        self.lsSource.append(audio)
        helper._write_lsStaticSource(self.lsSource)
        _audio = {'name': name, 'active': 1}
        self.bottom_left.list_source.add_source(_audio)

    def delete_source(self, index):
        if self.lsSource[index]['type'] == 'audio':
            self.bottom_left.list_mixer.del_source(self.lsSource[index]['idx'])
        del(self.lsSource[index])
        helper._write_lsStaticSource(self.lsSource)

    def openLogin(self):
        self.login_popup = Login(self)
        self.login_popup.open()

    def on_stop(self):
        if self.mainStream is not None:
            self.mainStream.release()

    def on_change_position(self, idx, pos_x, pos_y):
        for _s in self.lsSource:
            if _s['idx'] == idx:
                _s['pos_x'] = pos_x
                _s['pos_y'] = pos_y
                helper._write_lsStaticSource(self.lsSource)
                break
