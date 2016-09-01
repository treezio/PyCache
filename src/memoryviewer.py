import wx
import wx.stc as stc


class OverviewPanel(wx.Panel):

    def __init__(self, parent, grid):
        """Constructor"""
        self.grid = grid
        wx.Panel.__init__(self, parent, style=wx.NO_BORDER, size=(15, 0))
        self.SetBackgroundColour('gray')
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        """ Handles the wx.EVT_PAINT event for CustomCheckBox. """

        # If you want to reduce flicker, a good starting point is to
        # use wx.BufferedPaintDC.
        dc = wx.BufferedPaintDC(self)

        # It is advisable that you don't overcrowd the OnPaint event
        # (or any other event) with a lot of code, so let's do the
        # actual drawing in the Draw() method, passing the newly
        # initialized wx.BufferedPaintDC
        self.Draw(dc)

    def Draw(self, dc):
        """
        Actually performs the drawing operations, for the bitmap and
        for the text, positioning them centered vertically.
        """

        # Get the actual client size of ourselves
        width, height = self.GetClientSize()

        if not width or not height:
            # Nothing to do, we still don't have dimensions!
            return

        # Initialize the wx.BufferedPaintDC, assigning a background
        # colour and a foreground colour (to draw the text)
        backColour = self.GetBackgroundColour()
        backBrush = wx.Brush(backColour, wx.SOLID)
        dc.SetBackground(backBrush)
        dc.Clear()

        dc.SetBrush(wx.Brush('#c56c00'))
        dc.SetBackground(wx.Brush('#000000'))
        for row in range(self.grid.GetNumberRows()):
            dc.DrawRectangle(2, 2 + row * 15, 10, 10)

    def OnEraseBackground(self, event):
        """ Handles the wx.EVT_ERASE_BACKGROUND event for CustomCheckBox. """

        # This is intentionally empty, because we are using the combination
        # of wx.BufferedPaintDC + an empty OnEraseBackground event to
        # reduce flicker
        pass


class MemoryViewer(wx. Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        self.SetBackgroundColour('white')
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.pnl2 = stc.StyledTextCtrl(self)
        font = wx.Font(9, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        face = font.GetFaceName()
        size = font.GetPointSize()
        self.pnl2.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%s,size:%d" % (face, size))

        # pnl1 = OverviewPanel(self,pnl2)
        # hbox.Add(pnl1, 0, wx.EXPAND | wx.ALL, 3)
        hbox.Add(self.pnl2, 1, wx.EXPAND | wx.ALL, 3)
        self.SetSizer(hbox)
