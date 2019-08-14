class P300:
    def __init__(self, parent, p300):
        self.PV325 = p300["PV325"] or ""
        self.PP300 = p300["PP300"] or 0
        self.FO100 = p300["FO100"] or 0
        self.FT300 = p300["FT300"] or 0
        self.PO322 = p300["PO322"] or {}
        self.PO323 = p300["PO323"] or {}
