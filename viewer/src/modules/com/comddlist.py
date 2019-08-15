import tkinter as tk
from tkinter import messagebox
from src.modules.custom import DDList, VerticalScrolledFrame
from src.utils import helper
from src.modules.custom import ToolTip
from PIL import Image, ImageTk
from src.constants import UI


class COMDDList(tk.Frame):
    