from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

class SelectableGrid(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    """ Adds selection and focus behaviour to the view. """

class SelectableBox(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """