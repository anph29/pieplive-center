from kivy.uix.recycleview import RecycleView
import src.utils.helper as helper
from kivy.properties import StringProperty

class ListMedia(RecycleView):
 
    def __init__(self, **kwargs):
        super(ListMedia, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_video()]

    def remove(self, index):
        if self.data:
            self.data.pop(index)
            helper._write_video(self.clean_data_to_save_json())

    def clean_data_to_save_json(self):
        return list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type']},
                list(self.data)
            )
        )

    def refresh_list(self):
        self.set_data()

class ListImage(RecycleView):
 
    def __init__(self, **kwargs):
        super(ListImage, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_image()]

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

class ListCamera(RecycleView):

    def __init__(self, **kwargs):
        super(ListCamera, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_lscam()]

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

class ListPresenter(RecycleView):

    def __init__(self, **kwargs):
        super(ListPresenter, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_ls_presenter()]

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

class ListSchedule(RecycleView):

    def __init__(self, **kwargs):
        super(ListSchedule, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_schedule()]

    def get_data(self):
        return self.data

    def remove(self, index):
        if self.data:
            self.data.pop(index)
            helper._write_schedule(self.clean_data_to_save_json()) 

    def clean_data_to_save_json(self):
        return list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'], 'type': cam['type'], 'duration': cam['duration']},
                list(self.data)
            )
        )
    
    def refresh_list(self):
        self.set_data()

    def getCurrentIndex(self):
        for child in self.children[0].children:
            if child.selected:
                return child.index
        return -1
    
    def setSelected(self,index):
        for child in self.children[0].children:
            if child.index == index:
                child.selected = True
            else:
                child.selected = False
