from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from src.modules.bottomleft.bottomleft import TextDialog
from src.modules.bottomleft.bottomleft import ImageDialog
# from src.modules.bottomleft.bottomleft import AudioDialog
from src.modules.custom.addschedule import AddSchedule
from src.modules.kvsetting import KVSetting
from src.modules.mainstream import MainStream
from src.utils import helper, scryto
from kivy.lang import Builder
import sounddevice as sd

Builder.load_file('src/ui/main.kv')

class MainView(Widget):
    mainStream = ObjectProperty()
    bottom_left = ObjectProperty()
    btn_start = ObjectProperty()
    btn_display_mini = ObjectProperty()
    btn_switch = ObjectProperty()
    login_popup = ObjectProperty()
    right_content = ObjectProperty()
    videoBuffer = ObjectProperty()
    showMiniD = BooleanProperty(False)
    switchDisplay = BooleanProperty(False)
    idSoundDevice = StringProperty('')
    loading = BooleanProperty(False)
    loadingMini = BooleanProperty(False)
    presenterAuto = BooleanProperty(True)
    autoStop = BooleanProperty(False)
    mainDisplayStt = BooleanProperty(False)
    miniDisplayStt = BooleanProperty(False)
    streamServer = StringProperty('')
    streamKey = StringProperty('')

    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.lsAudio = []
        self.lsSource = []
        self.f_width = 1280
        self.f_height = 720
        self.setting = None
        self.src_selecting = ''# dang chay source cua list nao

    def on_start(self):
        self.mainStream._load()
        self.mainStream.f_parent = self
        self.bottom_left.f_parent = self
        self.right_content.f_parent = self
        self.setting = helper._load_setting()
        if self.setting['ouput_resolution'] is not None:
            self.f_width = self.mainStream.f_width = self.setting['ouput_resolution'][0]
            self.f_height = self.mainStream.f_height = self.setting['ouput_resolution'][1]
        if self.setting['vbitrate'] is not None:
            self.v_bitrate = self.mainStream.v_bitrate = self.setting['vbitrate']
        if self.setting['stream_server'] is not None:
            self.streamServer = self.setting['stream_server']
        if self.setting['stream_key'] is not None:
            self.streamKey = self.setting['stream_key']

        self.mainStream.urlStream = self.streamServer + self.streamKey
        self.initAudio()
        self.initSource()
        self.bottom_left.list_mixer.set_source(self.lsAudio)
        self.init_right_content_media()
        self.init_right_content_image()
        self.init_right_content_audio()
        self.init_right_content_cam()
        self.init_right_content_presenter()
        self.init_right_content_schedule()

    def init_right_content_media(self):
        self.right_content.tab_media.ls_media.set_data()
        
    def init_right_content_image(self):
        self.right_content.tab_image.ls_image.set_data()

    def init_right_content_audio(self):
        self.right_content.tab_audio.ls_audio.set_data()

    def init_right_content_cam(self):
        self.right_content.tab_camera.ls_camera.set_data()

    def init_right_content_presenter(self):
        self.right_content.tab_presenter.ls_presenter.set_data()

    def init_right_content_schedule(self):
        self.right_content.tab_schedule.ls_schedule.set_data()

    def right_content_schedule_refresh(self):
        self.right_content.tab_schedule.ls_schedule.refresh_list()

    def initAudio(self):
        try:
            self.audios = sd.query_devices(kind='input')
            if self.audios is not None:
                if 'Realtek High Defini' in self.audios['name']:
                    self.audios['name'] += 'tion Audio)'
                self.idSoundDevice = scryto.hash_md5_with_time(self.audios['name'].replace('\\', '/'))
                _audio = {
                    'id': self.idSoundDevice,
                    'name': self.audios['name'],
                    'src': self.audios['name'],
                    'volume': 100
                }
                self.lsAudio.append(_audio)
                self.changeAudio(self.audios['name'])
        except Exception as e:
            print("Exception:", e)

    def initSource(self):
        self.lsSource = helper._load_lsStaticSource()
        for idx, _s in enumerate(self.lsSource):
            if 'id' not in _s:
                _s['id'] = scryto.hash_md5_with_time('')
                self.lsSource[idx]['id'] = _s['id']
            if _s['type'] == 'text':
                self.mainStream.show_text( _s['id'], _s['label'], _s['font'], _s['size'],
                                        _s['color'], _s['pos_x'], _s['pos_y'], _s['active'], True)
            elif _s['type'] == 'image':
                self.mainStream.show_image( _s['id'], _s['src'], _s['pos_x'], _s['pos_y'], _s['width'], _s['height'], _s['active'], True)

        self.bottom_left.list_source.set_source(self.lsSource)

    def add_mixer(self, index, name, src, volume):
        if index == -1:
            audio = {
                "id": scryto.hash_md5_with_time(src.replace('\\', '/')),
                "type": "audio",
                "active": 0,
                "name": name,
                "src": src,
                "volume": volume
            }
            self.lsSource.append(audio)
            helper._write_lsStaticSource(self.lsSource)
            self.bottom_left.list_source.add_source(audio)
        else:
            self.lsSource[index]['name'] = name
            self.lsSource[index]['src'] = src
            self.lsSource[index]['volume'] = volume
            self.bottom_left.list_source.update_source(index,{"name":name, "active": self.lsSource[index]["active"]})
            self.bottom_left.list_mixer.update_source({'id': self.lsSource[index]['id'],'name': name,'src': src,'volume': volume})

    def changeSrc(self, data_src, data_type):
        if bool(data_src) and self.mainStream is not None:
            self.mainStream._set_capture(data_src, data_type, False)

    def changeSrcMini(self, data_src, data_type):
        if bool(data_src) and self.mainStream is not None:
            self.mainStream._set_captureMini(data_src, data_type, False)

    def changeAudio(self, value):
        if value is not None and self.mainStream is not None:
            self.mainStream.set_device_audio(value)

    def changeAudioVolume(self, id, volume):
        if self.mainStream is not None:
            self.mainStream.on_change_Volume(id, volume)

    def addPresenting(self, item):
        self.bottom_left.list_presenting.add_source(item)

    def deletePresenting(self, _id):
        self.bottom_left.list_presenting.del_source(_id)

    def change_auto_stop(self, val):
        self.autoStop = val

    def main_display_status(self, val):
        self.mainDisplayStt = val
        if self.mainStream.isStream is True:
            if self.mainDisplayStt is False and self.miniDisplayStt is False and self.right_content.tab_presenter.ls_presenter.get_number_active() == 0 :
                self.triggerStop()

    def mini_display_status(self, val):
        self.miniDisplayStt = val
        if self.mainStream.isStream is True:
            if self.mainDisplayStt is False and self.miniDisplayStt is False and self.right_content.tab_presenter.ls_presenter.get_number_active() == 0 :
                self.triggerStop()

    def start_stream(self):
        if self.mainStream.isStream is False:
            if len(self.streamServer) == 0 or len(self.streamKey) == 0:
                return False
            self.mainStream.set_url_stream(self.streamServer + self.streamKey)
            if bool(self.mainStream.prepare()):
                self.mainStream.startStream()
                self.btn_start.text = "Stop"
                self.btn_start.background_color = .29, .41, .15, 0.9

        elif self.mainStream.isStream is True:
            self.mainStream.stopStream()
            self.btn_start.text = "Start"
            self.btn_start.background_color = .29, .41, .55, 1

    def save_setting(self, stream_server, stream_key):
        if self.setting['stream_server'] is not None:
            self.streamServer = self.setting['stream_server'] = stream_server
        if self.setting['stream_key'] is not None:
            self.streamKey = self.setting['stream_key'] = stream_key
        self.mainStream.urlStream = self.streamServer + self.streamKey
        helper._write_setting(self.setting)

    def show_mini_display(self):
        if self.showMiniD is False:
            self.showMiniD = True
            self.btn_display_mini.text = "Hide Display Mini"
            self.btn_display_mini.background_color = .29, .41, .15, 0.9
            self.mainStream.show_camera_mini()
        else:
            self.showMiniD = False
            self.btn_display_mini.text = "Show Display mini"
            self.btn_display_mini.background_color = .29, .41, .55, 1
            self.mainStream.hide_camera_mini()

        self.switchDisplay = False
        self.btn_switch.background_color = .29, .41, .55, 1

    def switch_display(self):
        if self.showMiniD is True:
            if self.switchDisplay is False:
                self.switchDisplay = True
                self.btn_switch.background_color = .29, .41, .15, 0.9
            else:
                self.switchDisplay = False
                self.btn_switch.background_color = .29, .41, .55, 1
            self.mainStream.switch_display()

    def switch_display_auto(self):
        if self.showMiniD is True:
            if self.switchDisplay is False:
                self.switchDisplay = True
                self.btn_switch.background_color = .29, .41, .15, 0.9
                self.mainStream.show_camera_mini()
            else:
                self.switchDisplay = False
                self.btn_switch.background_color = .29, .41, .55, 1
                self.mainStream.hide_camera_mini()
            self.mainStream.switch_display_auto()

    def triggerStop(self):
        self.mainStream.stopStream()
        self.btn_start.text = "Start"
        self.btn_start.background_color = .29, .41, .55, 1

    def on_off_source(self, index, value):
        ite = self.lsSource[index]
        self.mainStream.on_off_source(ite['id'], value)
        self.lsSource[index]["active"] = value
        helper._write_lsStaticSource(self.lsSource)

    def openSetting(self):
        self.settingPop = KVSetting(self)
        self.settingPop.open()

    def add_source(self, type):
        if type == 'IMAGE':
            obj = ImageDialog(self)
            obj.open()
        elif type == 'TEXT':
            obj = TextDialog(self)
            obj.open()

    def add_text(self, index, name, label, font, size, color, pos_x, pos_y):
        if index == -1:
            text = {
                "id": scryto.hash_md5_with_time(label.replace('\\', '/')),
                "type": "text",
                "active": 1,
                "name": name,
                "label": label,
                "pos_x": pos_x,
                "pos_y": pos_y,
                "font": font,
                "size": int(size),
                "color": color,
                "shadow_color": None,
                "shadow_x": 0,
                "shadow_y": 0,
                "box": None,
                "box_color": None
            }
            self.lsSource.append(text)
            helper._write_lsStaticSource(self.lsSource)
            self.bottom_left.list_source.add_source(text)
            self.mainStream.show_text(text['id'], label, font, size, color, pos_x, pos_y, 1, True)
        else:
            self.lsSource[index]['name'] = name
            self.lsSource[index]['label'] = label
            self.lsSource[index]['font'] = font
            self.lsSource[index]['size'] = int(size)
            self.lsSource[index]['color'] = color
            helper._write_lsStaticSource(self.lsSource)
            self.bottom_left.list_source.update_source(index,{"name":name, "active": self.lsSource[index]["active"]})
            self.mainStream.show_text(self.lsSource[index]['id'],label, font, int(size), color, pos_x, pos_y, self.lsSource[index]["active"], False)

    def add_image(self, index, name, src, pos_x, pos_y, width, height):
        if index == -1:
            image = {
                "id": scryto.hash_md5_with_time(src.replace('\\', '/')),
                "type": "image",
                "active": 1,
                "name": name,
                "src": src,
                "pos_x": pos_x,
                "pos_y": pos_y,
                "width": int(width),
                "height": int(height),
                "timeStart": None,
                "timeEnd": None
            }
            self.lsSource.append(image)
            helper._write_lsStaticSource(self.lsSource)
            self.bottom_left.list_source.add_source(image)
            self.mainStream.show_image(image['id'], src, pos_x, pos_y, width, height, 1,True)
        else:
            self.lsSource[index]['name'] = name
            self.lsSource[index]['src'] = src
            self.lsSource[index]['width'] = int(width)
            self.lsSource[index]['height'] = int(height)
            helper._write_lsStaticSource(self.lsSource)
            self.bottom_left.list_source.update_source(index,{"name":name, "active": self.lsSource[index]["active"]})
            self.mainStream.show_image(self.lsSource[index]['id'], src, pos_x, pos_y, int(width), int(height), self.lsSource[index]["active"], False)

    def delete_source(self, index):
        if self.lsSource[index]['type'] == 'audio':
            self.bottom_left.list_mixer.del_source(self.lsSource[index]['id'])
        del(self.lsSource[index])
        helper._write_lsStaticSource(self.lsSource)

    def on_stop(self):
        if self.mainStream is not None:
            self.mainStream.release()
        if self.right_content is not None:
            self.right_content.tab_presenter.ls_presenter.stopListenerStream()

    def on_change_position(self, _id, pos_x, pos_y):
        for _s in self.lsSource:
            if _s['id'] == _id:
                _s['pos_x'] = pos_x
                _s['pos_y'] = pos_y
                helper._write_lsStaticSource(self.lsSource)
                break

    def on_edit_source(self,index):
        ite = self.lsSource[index]
        if ite['type'] == 'image':
            obj = ImageDialog(self, ite, index)
            obj.open()
        elif ite['type'] == 'text':
            obj = TextDialog(self, ite, index)
            obj.open()
    
    def open_add_schedule(self, data):
        self.add_schedule_pop = AddSchedule(self,data)
        self.add_schedule_pop.open()

    def refresh_select_source(self, type):
        if self.src_selecting != '' and self.src_selecting != type:
            if self.src_selecting == 'VIDEO':
                self.right_content.tab_media.ls_media.item_playing = ''
                self.right_content.tab_media.ls_media.set_data()
            elif self.src_selecting == 'IMAGE':
                self.right_content.tab_image.ls_image.item_playing = ''
                self.right_content.tab_image.ls_image.set_data()
            elif self.src_selecting == 'CAMERA':
                self.right_content.tab_camera.ls_camera.item_playing = ''
                self.right_content.tab_camera.ls_camera.set_data()
            elif self.src_selecting == 'PRESENTER':
                self.right_content.tab_presenter.ls_presenter.item_playing = ''
                self.right_content.tab_presenter.ls_presenter.set_data()
            elif self.src_selecting == 'SCHEDULE':
                self.right_content.tab_schedule.ls_schedule.item_playing = ''
                self.right_content.tab_schedule.ls_schedule.set_data()
        self.src_selecting = type