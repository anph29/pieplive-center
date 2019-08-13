from tkinter import Label


class PLabel(Label):
    """A type of Label that adds an ellipsis to overlong text"""

    def __init__(self, master=None, elipsis=50, text=None, width=None, **kwargs):
        if text and len(text) > elipsis:
            text = text[: elipsis - 3] + "..."
        Label.__init__(self, master, text=text, width=width, **kwargs)
