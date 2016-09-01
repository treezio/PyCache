
import wx 
import wx.stc as stc

class TraceEditor(stc.StyledTextCtrl):
    def __init__(self, parent, style=wx.SIMPLE_BORDER):
        """
        Constructor
        
        """
        stc.StyledTextCtrl.__init__(self, parent, style=style)
        self._styles = [None]*32
        self._free = 1

