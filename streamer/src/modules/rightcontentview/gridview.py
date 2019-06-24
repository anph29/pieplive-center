from src.modules.recyclelayout.recyclegridlayout import SelectableGrid
import src.utils.helper as helper


class GridCamera(SelectableGrid):
    """ Adds selection and focus behaviour to the view. """

    # def select_node(self, node):
    #     helper.getApRoot().changeSrc(
    #         self.children[node].kvcam.capture
    #     )
    #     return super(GridCamera, self).select_node(node)

    def sort(self):
        self.parent.data = sorted(self.parent.data, key=lambda x: x['value'])

    def insert(self, value):
        self.parent.data.insert(0, {'value': value or 'default value'})

    # def update(self, value):
    #     if self.parent.data:
    #         self.parent.data[0]['value'] = value or 'default new value'
    #         self.parent.refresh_from_data()

    def remove(self, index):
        if self.parent.data:
            self.parent.data.pop(index)
            # helper._write_lscam(self.clean_data_to_save_json())

    def clean_data_to_save_json(self):
        return list(
            map(
                lambda cam: {'name': cam['name'], 'url': cam['url']},
                list(self.parent.data)
            )
        )
