from src.modules.recyclelayout.recyclegridlayout import SelectableGrid, SelectableBox
import src.utils.helper as helper


class GridCamera(SelectableGrid):
    """ Adds selection and focus behaviour to the view. """

    def sort(self):
        self.parent.data = sorted(self.parent.data, key=lambda x: x['value'])

    def insert(self, value):
        self.parent.data.insert(0, {'value': value or 'default value'})

class BoxCamera(SelectableBox):
    """ Adds selection and focus behaviour to the view. """

    def sort(self):
        self.parent.data = sorted(self.parent.data, key=lambda x: x['value'])

    def insert(self, value):
        self.parent.data.insert(0, {'value': value or 'default value'})
