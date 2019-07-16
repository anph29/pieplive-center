class AddToSchedule(object):
    useLocal = False
    addCamPopup = None
    error = False

    def __init__(self, parent):
        self.parent = parent

    def initGUI(self, evt):
        # first destroy
        if None is not self.addCamPopup:
            self.addCamPopup.destroy()
        self.addCamPopup = tk_helper.makePiepMePopup('Add Media', w=400, h=250, padx=0, pady=0)
        self.makeMasterTab()
    