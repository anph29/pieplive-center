#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *   # from x import * is bad practice
from tkinter.ttk import *

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind('<Configure>', self._configure_canvas)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)
        self.interior.bind('<Configure>', self._configure_interior)

    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the self.canvas
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())


    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta/120), "units")
    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar


if __name__ == "__main__":

    class SampleApp(Tk):
        def __init__(self, *args, **kwargs):
            root = Tk.__init__(self, *args, **kwargs)


            self.frame = VerticalScrolledFrame(root)
            self.frame.pack()
            self.label = Label(text="Shrink the window to activate the scrollbar.")
            self.label.pack()
            # buttons = []
            for i in range(10):
                # buttons.append(Button(self.frame.interior, text="Button " + str(i)))
                # buttons[-1].pack()
                Button(self.frame.interior, text="Button " + str(i)).pack()

    app = SampleApp()
    app.mainloop()