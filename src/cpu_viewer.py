
import wx
from traceeditor import TraceEditor


class CPU_Viewer(wx.Panel):
    style_start = 0
    style_length = 0
    style_number = 0

    def __init__(self, parent, module):
        super(wx.Panel, self).__init__(parent)

        self.SetBackgroundColour('white')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.pnl2 = TraceEditor(self)
        self.pnl2.LoadFile(module.trace_file)
        self.pnl2.SetCurrentPos(0)
        self.pnl2.StyleSetSpec(2, "back:#0000ff")

# GetCurLine
        hbox.Add(self.pnl2, 1, wx.EXPAND | wx.ALL, 3)
        self.SetSizer(hbox)

    def get_line_count(self):
        return self.pnl2.GetLineCount()

    def get_line(self, line):
        self.pnl2.StartStyling(self.style_start, 0xff)
        self.pnl2.SetStyling(self.style_length, self.style_number)
        self.style_start = self.pnl2.GetLineIndentPosition(line)
        self.style_length = self.pnl2.GetLineEndPosition(line) - self.style_start
        self.style_number = self.pnl2.GetStyleAt(self.style_start)
        self.pnl2.SetCurrentPos(self.style_start)
        self.pnl2.SetSelection(self.style_start, self.style_start)
        self.pnl2.StartStyling(self.style_start, 0xff)
        self.pnl2.SetStyling(self.style_length, 2)
        return self.pnl2.GetCurLine()
