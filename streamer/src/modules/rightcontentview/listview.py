from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
import datetime
from src.modules.custom.popup import PiepMeConfirmPopup
from src.utils import helper, firebase, store, kivyhelper
from src.modules.custom.linkaudio import LinkAudio
from src.modules import constants

class ListMedia(RecycleView):
    item_playing = ''
    item_playing_mini = ''
 
    def __init__(self, **kwargs):
        super(ListMedia, self).__init__(**kwargs)

    def set_data(self):
        self.data = list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type'], 
                'duration': cam['duration'] if 'duration' in cam else 0,
                'list': constants.LIST_TYPE_VIDEO,
                'active': (False,True) [cam['id'] == self.item_playing],
                'activeMini': (False,True) [cam['id'] == self.item_playing_mini],
                'choice':False},
                helper._load_video()
            )
        )

    def remove(self, index):
        if self.data:
            self.data.pop(index)
            helper._write_video(self.clean_data_to_save_json())

    def clean_data_to_save_json(self):
        return list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type'], 'duration': cam['duration']},
                list(self.data)
            )
        )

    def refresh_list(self):
        self.set_data()
        self.refresh_view()
    
    def remove_selected(self):
        PiepMeConfirmPopup(message='Are you sure to delete the selected source?',
                            callback_ok=self.process_del_selected,
                            callback_cancel=lambda: True)
                            
    def process_del_selected(self):
        temp = 0
        for child in self.children[0].children:
            if child.isCheckItem.active and child.selected == False:
                temp = 1
                if self.data:
                    self.data.pop(child.index)
        if temp == 1:
            helper._write_video(self.clean_data_to_save_json())

    def setPlayed(self,index):
        self.item_playing = self.data[index]['id']
        for obj in self.data:
            obj['active'] = False
        self.data[index]['active'] = True
        for child in self.children[0].children:
            if child.index == index:
                child.active = True
            else:
                child.active = False

    def setPlayedMini(self,index):
        self.item_playing_mini = self.data[index]['id']
        for obj in self.data:
            obj['activeMini'] = False
        self.data[index]['activeMini'] = True
        for child in self.children[0].children:
            if child.index == index:
                child.activeMini = True
            else:
                child.activeMini = False
    
    def refresh_view(self):
        try:
            for child in self.children[0].children:
                child.refresh_view_attrs(self,child.index, self.data[child.index])
        except:
            pass

class ListImage(RecycleView):
    item_playing = ''
    item_playing_mini = ''

    def __init__(self, **kwargs):
        super(ListImage, self).__init__(**kwargs)

    def set_data(self):
        self.data = list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type'], 
                'list':constants.LIST_TYPE_IMAGE,
                'active': (False,True) [cam['id'] == self.item_playing],
                'activeMini': (False,True) [cam['id'] == self.item_playing_mini],
                'choice':False},
                helper._load_image()
            )
        )

    def remove(self, index):
        if self.data:
            self.data.pop(index)
            helper._write_image(self.clean_data_to_save_json())

    def clean_data_to_save_json(self):
        return list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type']},
                list(self.data)
            )
        )

    def refresh_list(self):
        self.set_data()
        self.refresh_view()
    
    def remove_selected(self):
        PiepMeConfirmPopup(message='Are you sure to delete the selected source?',
                            callback_ok=self.process_del_selected,
                            callback_cancel=lambda: True)
                            
    def process_del_selected(self):
        temp = 0
        for child in self.children[0].children:
            if child.isCheckItem.active and child.selected == False:
                temp = 1
                if self.data:
                    self.data.pop(child.index)
        if temp == 1:
            helper._write_image(self.clean_data_to_save_json())

    def setPlayed(self,index):
        self.item_playing = self.data[index]['id']
        for obj in self.data:
            obj['active'] = False
        self.data[index]['active'] = True
        for child in self.children[0].children:
            if child.index == index:
                child.active = True
            else:
                child.active = False

    def setPlayedMini(self,index):
        self.item_playing_mini = self.data[index]['id']
        for obj in self.data:
            obj['activeMini'] = False
        self.data[index]['activeMini'] = True
        for child in self.children[0].children:
            if child.index == index:
                child.activeMini = True
            else:
                child.activeMini = False

    def refresh_view(self):
        try:
            for child in self.children[0].children:
                child.refresh_view_attrs(self,child.index, self.data[child.index])
        except:
            pass

class ListAudios(RecycleView):

    def __init__(self, **kwargs):
        super(ListAudios, self).__init__(**kwargs)

    def set_data(self):
        self.data = list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type'],
                'volume':cam['volume'],
                'active': cam['active'] if 'active' in cam else False,
                'list':'AUDIO'},
                helper._load_ls_audio()
            )
        )

    def get_data(self):
        return self.data

    def remove(self, index):
        if self.data:
            self.data.pop(index)
            helper._write_lsaudio(self.clean_data_to_save_json())

    def clean_data_to_save_json(self):
        return list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type'], 'volume':cam['volume'],'active': cam['active']},
                list(self.data)
            )
        )

    def refresh_list(self):
        self.set_data()
        self.refresh_view()
    
    def remove_selected(self):
        PiepMeConfirmPopup(message='Are you sure to delete the selected source?',
                            callback_ok=self.process_del_selected,
                            callback_cancel=lambda: True)
                            
    def process_del_selected(self):
        temp = 0
        for child in self.children[0].children:
            if child.isCheckItem.active and child.selected == False:
                temp = 1
                if self.data:
                    self.data.pop(child.index)
        if temp == 1:
            helper._write_lsaudio(self.clean_data_to_save_json())

    def setActive(self,index,val):
        self.data[index]['active'] = val
        helper._write_lsaudio(self.clean_data_to_save_json())
        kivyhelper.getApRoot().mainStream.refresh_stream()

    def refresh_view(self):
        try:
            for child in self.children[0].children:
                child.refresh_view_attrs(self,child.index, self.data[child.index])
        except:
            pass

class ListCamera(RecycleView):
    item_playing = ""
    item_playing_mini = ""
    def __init__(self, **kwargs):
        super(ListCamera, self).__init__(**kwargs)

    def set_data(self):
        self.data = list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type'], 
                'list':constants.LIST_TYPE_CAMERA,
                'active': (False,True) [cam['id'] == self.item_playing],
                'activeMini': (False,True) [cam['id'] == self.item_playing_mini],
                'choice':False},
                helper._load_lscam()
            )
        )

    def remove(self, index):
        if self.data:
            self.data.pop(index)
            helper._write_lscam(self.clean_data_to_save_json())

    def clean_data_to_save_json(self):
        return list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type']},
                list(self.data)
            )
        )

    def refresh_list(self):
        self.set_data()
        self.refresh_view()
    
    def remove_selected(self):
        PiepMeConfirmPopup(message='Are you sure to delete the selected source?',
                            callback_ok=self.process_del_selected,
                            callback_cancel=lambda: True)
                            
    def process_del_selected(self):
        temp = 0
        for child in self.children[0].children:
            if child.isCheckItem.active and child.selected == False:
                temp = 1
                if self.data:
                    self.data.pop(child.index)
        if temp == 1:
            helper._write_lscam(self.clean_data_to_save_json())

    def setPlayed(self,index):
        self.item_playing = self.data[index]['id']
        for obj in self.data:
            obj['active'] = False
        self.data[index]['active'] = True
        for child in self.children[0].children:
            if child.index == index:
                child.active = True
            else:
                child.active = False

    def setPlayedMini(self,index):
        self.item_playing_mini = self.data[index]['id']
        for obj in self.data:
            obj['activeMini'] = False
        self.data[index]['activeMini'] = True
        for child in self.children[0].children:
            if child.index == index:
                child.activeMini = True
            else:
                child.activeMini = False

    def refresh_view(self):
        try:
            for child in self.children[0].children:
                child.refresh_view_attrs(self,child.index, self.data[child.index])
        except:
            pass

class ListPresenter(RecycleView):
    item_playing = ''
    item_playing_mini = ''
    item_choice = '0'
    listenerStream = None
    is_auto = BooleanProperty(True)
    switch_proc = None

    def __init__(self, **kwargs):
        super(ListPresenter, self).__init__(**kwargs)

    def onChangePresenter(self, presenter):
        #choice status
        if int(self.item_choice) == presenter:
            pass
        else:
            if presenter == 0 and kivyhelper.getApRoot().presenterAuto is True and kivyhelper.getApRoot().mainStream.isStream is True and kivyhelper.getApRoot().modeStream == 'NORMAL':
                if self.switch_proc is not None:
                    self.switch_proc.cancel()
                
                idx = -1
                for child in self.children[0].children:
                    if child.id == self.item_choice:
                        idx = child.index
                if idx != -1:
                    for child in self.children[0].children:
                        if child.index != idx and child.playable:
                            presenter = int(child.id)
                            firebase.makeChangePresenter(presenter)
                            self.switch_proc = Clock.schedule_once(lambda x: kivyhelper.getApRoot().switch_display_auto(0),kivyhelper.getApRoot().delaySwitchDisplay)
                            kivyhelper.getApRoot().delaySwitchDisplay += 2
                            break
            self.item_choice = str(presenter)

            for obj in self.data:
                obj['list'] = constants.LIST_TYPE_PRESENTER
                if int(obj['id']) == int(presenter):
                    obj['choice'] = True
                else:
                    obj['choice'] = False
            
            for child in self.children[0].children:
                child.listType = constants.LIST_TYPE_PRESENTER
                if int(child.id) == int(presenter):
                    child.choice = True
                else:
                    child.choice = False

    def onChangeLN510(self, data):
        #play able status
        if bool(data):
            if '_id' in data:  # case change: get single data
                self.changeStatePresenter(data)
            else:  # case init: get multi data
                for k in list(data.keys()):
                    self.changeStatePresenter(data[k])

    def changeStatePresenter(self, media):
        _id = int(media['_id'])
        ln510 = int(media['LN510'])
        for m in self.data:
            if int(m['id']) == _id:
                if ln510 == 2:
                    m['playable'] = True
                    item = {'id':m['id'],'name':m['name']}
                    kivyhelper.getApRoot().addPresenting(item)
                else:
                    kivyhelper.getApRoot().deletePresenting(m['id'])
                    m['playable'] = False
        self.refresh_view()

    def choice_play(self, index):
        if self.data[index]['id'] == self.item_choice:
            firebase.makeChangePresenter(0)
            self.item_choice = "0"
            self.data[index]['choice'] = False
            for child in self.children[0].children:
                child.choice = False
                child.listType=constants.LIST_TYPE_PRESENTER
        else:
            firebase.makeChangePresenter(int(self.data[index]['id']))
            self.item_choice = self.data[index]['id']
            for obj in self.data:
                obj['choice'] = False
                obj['list'] = constants.LIST_TYPE_PRESENTER
            self.data[index]['choice'] = True
            for child in self.children[0].children:
                child.listType=constants.LIST_TYPE_PRESENTER
                if child.index == index:
                    child.choice = True
                else:
                    child.choice = False

    def set_data(self):
        self.data = list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type'], 
                'rtmp': cam['rtmp'] if 'rtmp' in cam else cam['url'],
                'list':constants.LIST_TYPE_PRESENTER,
                'active': (False,True) [cam['id'] == self.item_playing],
                'activeMini': (False,True) [cam['id'] == self.item_playing_mini],
                'choice': (False,True) [cam['id'] == self.item_choice],
                'playable': False},
                helper._load_ls_presenter()
            )
        )

    def remove(self, index):
        if self.data:
            self.data.pop(index)
            helper._write_lspresenter(self.clean_data_to_save_json())

    def clean_data_to_save_json(self):
        return list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type']},
                list(self.data)
            )
        )

    def refresh_list(self):
        self.set_data()
        kivyhelper.getApRoot().turnOnObserver(1)

    def remove_selected(self):
        PiepMeConfirmPopup(message='Are you sure to delete the selected source?',
                            callback_ok=self.process_del_selected,
                            callback_cancel=lambda: True)
                            
    def process_del_selected(self):
        temp = 0
        for child in self.children[0].children:
            if child.isCheckItem.active and child.selected == False:
                temp = 1
                if self.data:
                    self.data.pop(child.index)
        if temp == 1:
            helper._write_lspresenter(self.clean_data_to_save_json())
    
    def setPlayed(self,index):
        self.item_playing = self.data[index]['id']
        for obj in self.data:
            obj['active'] = False
        self.data[index]['active'] = True
        for child in self.children[0].children:
            if child.index == index:
                child.active = True
            else:
                child.active = False

    def setPlayedMini(self,index):
        self.item_playing_mini = self.data[index]['id']
        for obj in self.data:
            obj['activeMini'] = False
        self.data[index]['activeMini'] = True
        for child in self.children[0].children:
            if child.index == index:
                child.activeMini = True
            else:
                child.activeMini = False

    def refresh_view(self):
        try:
            for child in self.children[0].children:
                child.refresh_view_attrs(self,child.index, self.data[child.index])
        except:
            pass
    
    def change_presenter_auto(self, _val):
        kivyhelper.getApRoot().change_presenter_auto(_val)

    def get_number_active(self):
        num = 0
        for m in self.data:
            if m['playable'] is True:
                num = num + 1
        return num

    def check_is_online(self, _id):
        for obj in self.data:
            if str(obj['id']) == str(_id) and obj['playable'] is True:
                return True
        return False

        
class ListSchedule(RecycleView):
    item_playing = ""
    total_time = StringProperty("00:00:00")

    def __init__(self, **kwargs):
        super(ListSchedule, self).__init__(**kwargs)

    def set_data(self):
        self.data = list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type'], 'duration': cam['duration'], 
                'timepoint': cam['timepoint'] if 'timepoint' in cam else 0,
                'audio': cam['audio'] if 'audio' in cam else '',
                'audio_name': cam['audio_name'] if 'audio_name' in cam else '',
                'list':constants.LIST_TYPE_SCHEDULE,
                'active': (False,True) [cam['id'] == self.item_playing]},
                helper._load_schedule()
            )
        )
        self.getTotalTime()

    def get_data(self):
        self.set_data()
        return self.data

    def remove(self, index):
        if self.data:
            self.data.pop(index)
            helper._write_schedule(self.clean_data_to_save_json())

    def clean_data_to_save_json(self):
        return list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type'], 'duration': cam['duration'], 'timepoint': cam['timepoint'],'audio': cam['audio'],'audio_name': cam['audio_name']},
                list(self.data)
            )
        )
    
    def refresh_list(self):
        self.set_data()
        self.refresh_view()
        self.makeTimePointChange()
        self.refresh_view()

    def getCurrentIndex(self):
        for child in self.children[0].children:
            if child.active:
                return child.index
        return -1

    def setSelected(self,index):
        for child in self.children[0].children:
            if child.index == index:
                child.selected = True
            else:
                child.selected = False

    def setPlayed(self,index):
        self.item_playing = self.data[index]['id']
        for obj in self.data:
            obj['active'] = False
        self.data[index]['active'] = True
        for child in self.children[0].children:
            if child.index == index:
                child.active = True
            else:
                child.active = False
    
    def up_list(self,index):
        if index == 0:
            return True
        self.data[index-1], self.data[index] = self.data[index], self.data[index-1]
        self.refresh_view()
        self.makeTimePointChange()

    def down_list(self,index):
        if index == len(self.data)-1:
            return True
        self.data[index+1], self.data[index] = self.data[index], self.data[index+1]
        self.refresh_view()
        self.makeTimePointChange()

    def remove_selected(self):
        PiepMeConfirmPopup(message='Are you sure to delete the selected source?',
                            callback_ok=self.process_del_selected,
                            callback_cancel=lambda: True)

    def process_del_selected(self):
        temp = 0
        for child in self.children[0].children:
            if child.isCheckItem.active and child.active == False:
                temp = 1
                if self.data:
                    self.data.pop(child.index)
        if temp == 1:
            helper._write_schedule(self.clean_data_to_save_json())
            self.getTotalTime()
    
    def getTotalTime(self):
        tt = 0
        for item in self.data:
            tt += item['duration']
        self.total_time = helper.convertSecNoToHMS(tt)

    def makeTimePoint(self,index):
        helper.calc_schedule_runtime(index)
        self.set_data()
        self.refresh_view()

    def makeTimePointChange(self):
        idx = self.getCurrentIndex()
        if idx != -1:
            s = self.data[idx]['timepoint']
            for i, obj in enumerate(self.data):
                if i < idx:
                    self.data[i]['timepoint'] = 0
                if i > idx:
                    s += self.data[i-1]['duration']
                    if s > 86400:
                        s = s - 86400
                    self.data[i]['timepoint'] = s
        else:
            self.data = helper.calc_schedule_runtime(0,self.data)
        helper._write_schedule(self.clean_data_to_save_json())
        self.refresh_view()

    def refresh_view(self):
        try:
            for child in self.children[0].children:
                child.refresh_view_attrs(self,child.index, self.data[child.index])
        except:
            pass
    
    def link_audio(self, _parent, idx, src):
        _audio = LinkAudio(_parent,idx, src, self.link_audio_result)
        _audio.open()

    def link_audio_result(self, name, src, idx):
        self.data[idx]['audio_name'] = name
        self.data[idx]['audio'] = src
        helper._write_schedule(self.clean_data_to_save_json())
        self.refresh_view()