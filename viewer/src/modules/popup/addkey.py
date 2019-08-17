import tkinter as tk
from tkinter import ttk
from src.utils import tk_helper, helper, scryto
from src.constants import UI
import re
import urllib


class PopupAddKey(object):
    def __init__(self, parent, data=None):
        self.popup = None
        self.parent = parent
        self.key = data

    def setupData(self, edit=False):
        if edit:
            self.label = self.key["label"]
            self.id = self.key["id"]
            self.keyA = self.key["key_a"]
            self.keyB = self.key["key_b"]
            self.P300 = self.key["P300"]
            self.play = self.key["PLAY"]
            self.p300 = self.key["P300"]
        else:
            self.id = scryto.hash_md5_with_time("new key")
            self.label = ""
            self.keyA = ""
            self.keyB = ""
            self.P300 = ""
            self.play = ""
            self.p300 = {}
        #

    def initGUI(self, edit=False):
        # first destroy
        if bool(self.popup):
            self.popup.destroy()
        self.popup = tk_helper.makePiepMePopup(
            "Key Stream", w=400, h=200, padx=0, pady=0
        )
        # var
        self.setupData(edit=edit)
        self.eLabel = tk.StringVar()
        self.eLabel.set(self.label)
        self.eKeyA = tk.StringVar()
        self.eKeyA.set(self.keyA)
        self.eKeyB = tk.StringVar()
        self.eKeyB.set(self.keyB)
        #
        wrapper = tk.Frame(self.popup)
        wrapper.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # 1. Label
        fLabel = tk.Frame(wrapper, pady=10, padx=20)
        fLabel.pack(side=tk.TOP, fill=tk.X)
        lLabel = tk.Label(fLabel, text="Label:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lLabel.pack(side=tk.LEFT, fill=tk.Y)
        label = tk.Entry(
            fLabel, textvariable=self.eLabel, width=100, borderwidth=5, relief=tk.FLAT
        )
        label.bind("<FocusIn>", lambda args: label.select_range("0", tk.END))
        label.pack(side=tk.LEFT, fill=tk.X, padx=(10, 0))
        # 2. Key A
        fKeyA = tk.Frame(wrapper, pady=10, padx=20)
        fKeyA.pack(side=tk.TOP, fill=tk.X)
        lKeyA = tk.Label(fKeyA, text="KeyA:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lKeyA.pack(side=tk.LEFT, fill=tk.Y)
        keyA = tk.Entry(
            fKeyA, textvariable=self.eKeyA, width=100, borderwidth=5, relief=tk.FLAT
        )
        keyA.bind("<FocusIn>", lambda args: keyA.select_range("0", tk.END))
        keyA.pack(side=tk.LEFT, fill=tk.X, padx=(10, 0))
        # 2. Key B
        fKeyB = tk.Frame(wrapper, pady=10, padx=20)
        fKeyB.pack(side=tk.TOP, fill=tk.X)
        lKeyB = tk.Label(fKeyB, text="KeyB:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lKeyB.pack(side=tk.LEFT, fill=tk.Y)
        keyB = tk.Entry(
            fKeyB, textvariable=self.eKeyB, width=100, borderwidth=5, relief=tk.FLAT
        )
        keyB.bind("<FocusIn>", lambda args: keyB.select_range("0", tk.END))
        keyB.pack(side=tk.LEFT, fill=tk.X, padx=(10, 0))
        # 4. Button
        fBtn = tk.Frame(wrapper, pady=10, padx=20)
        btnCancel = tk.Button(
            fBtn, text="Cancel", bd=2, relief=tk.RAISED, command=self.popup.destroy
        )
        btnCancel.configure(width=7)
        btnCancel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        btnOk = tk.Button(
            fBtn,
            text="OK",
            bd=2,
            bg="#ff2d55",
            fg="#fff",
            relief=tk.RAISED,
            command=self.onSaveEdit if edit else self.onSaveNew,
        )
        btnOk.configure(width=7)
        btnOk.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        fBtn.pack(side=tk.BOTTOM, fill=tk.X)

    def onSaveNew(self):
        if self.canSave():
            self.parent.addKey(self.getDataToSave())
            self.popup.destroy()

    def onSaveEdit(self):
        if self.canSave():
            self.parent.saveEditKey(self.getDataToSave())
            self.popup.destroy()

    def canSave(self):
        return (
            0 < len(self.eLabel.get())
            and 0 < len(self.eKeyA.get())
            and 0 < len(self.eKeyB.get())
        )

    def getDataToSave(self):
        return {
            "id": self.id,
            "label": self.eLabel.get(),
            "key_a": self.eKeyA.get(),
            "key_b": self.eKeyB.get(),
            "PLAY": self.play,
            "P300": self.p300,
        }
