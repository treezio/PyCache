#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
ZetCode wxPython tutorial

In this example, we create a submenu and a menu
separator.

author: Jan Bodnar
website: www.zetcode.com
last modified: September 2011
'''

import wx
from wx import AboutBox
from wx.lib.splitter import MultiSplitterWindow
import wx.grid as gridlib
import wx.lib.mixins.listctrl as listmix
import os
import sys

ID_SPLITTER = 300


class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)

        files = os.listdir('.')
        self.InsertColumn(0, 'N')
        self.InsertColumn(1, 'K')
        self.InsertColumn(2, 'F')
        self.InsertColumn(3, 'D')
        self.InsertColumn(4, 'T')
        self.InsertColumn(5, 'Tam')
        self.InsertColumn(6, 'Dat')

        j = 0
        with open('dict_trazas_sanitized.csv', 'r') as csvfile:
            for line in csvfile:
                splitted_parts = line.split(",")
                self.InsertStringItem(sys.maxint, str(j + 1))
                self.SetStringItem(j, 1, splitted_parts[0])
                self.SetStringItem(j, 2, splitted_parts[1])
                self.SetStringItem(j, 3, splitted_parts[2])
                self.SetStringItem(j, 4, splitted_parts[3])
                if len(splitted_parts[4]) > 0:
                    self.SetStringItem(j, 5, str(splitted_parts[4]) + ' B')
                else:
                    self.SetStringItem(j, 5, '')

                if len(splitted_parts[5]) > 0:
                    self.SetStringItem(j, 6, splitted_parts[5])
                else:
                    self.SetStringItem(j, 6, '')

                if splitted_parts[0] == '!':
                    self.SetItemBackgroundColour(j, "yellow")
                elif splitted_parts[0] == '#':
                    self.SetItemBackgroundColour(j, "green")
                else:
                    self.SetItemBackgroundColour(j, "white")
                j = j + 1


class SamplePanel(wx.Panel):
    def __init__(self, parent, colour):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(colour)


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


class SubSamplePanel(SamplePanel):
    def __init__(self, parent, colour):
        super(SamplePanel, self).__init__(parent)

        self.SetBackgroundColour('white')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        pnl2 = gridlib.Grid(self)
        pnl2.CreateGrid(12, 8)
        pnl2.AutoSizeColumns()
        pnl2.SetRowLabelSize(1)
        pnl2.SetColLabelSize(1)
        pnl1 = OverviewPanel(self, pnl2)

        hbox.Add(pnl1, 0, wx.EXPAND | wx.ALL, 3)
        hbox.Add(pnl2, 1, wx.EXPAND | wx.ALL, 3)
        self.SetSizer(hbox)

trace_text = """# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
# D 0x00000001 L 8 foo
I 0xA0000000 S 16 bar
! D 0x04000050 L 352 3000
D 0xCA080003 S
"""


class CPUPanel(SamplePanel):
    def __init__(self, parent, colour):
        super(SamplePanel, self).__init__(parent)

        self.SetBackgroundColour('white')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        pnl2 = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        pnl2.SetValue(trace_text)
        pnl1 = OverviewPanel(self, pnl2)

        hbox.Add(pnl1, 0, wx.EXPAND | wx.ALL, 3)
        hbox.Add(pnl2, 1, wx.EXPAND | wx.ALL, 3)
        self.SetSizer(hbox)


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        "=================="
        " Creating Menubar "
        "=================="
        # importing menubar
        menubar = wx.MenuBar()
        # menu objects
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()
        simulationMenu = wx.Menu()
        # Adding menu
        menubar.Append(fileMenu, '&File')
        menubar.Append(simulationMenu, '&Simulation')
        menubar.Append(helpMenu, '&Help')
        # Submenu for simulation
        sim_submenu = wx.Menu()
        sim_submenu.Append(wx.ID_OPEN, '&Open Simulation File')
        sim_submenu.Append(wx.ID_SAVE, '&Save Simulation File')
        sim_submenu.Append(wx.ID_SAVEAS, '&Save Simulation File as...')
        sim_submenu.Append(wx.ID_CLEAR, '&Wipe current loaded Simulation File')

        # submenu for hardware configuration
        cfg_submenu = wx.Menu()
        cfg_submenu.Append(wx.ID_OPEN, '&Open Hardware Configuration File')
        cfg_submenu.Append(wx.ID_SAVE, '&Save Hardware Configuration File')
        cfg_submenu.Append(wx.ID_SAVEAS, '&Save Hardware Configuration File as...')
        cfg_submenu.Append(wx.ID_CLEAR, '&Wipe current Hardware Configuration')
        # File Menu
        fileMenu.AppendMenu(wx.ID_ANY, '&Simulation File', sim_submenu)
        fileMenu.AppendMenu(wx.ID_ANY, '&Hardware Configuration', cfg_submenu)
        # Adding Separator
        fileMenu.AppendSeparator()
        exit_ev = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Exit\tCtrl+E')
        fileMenu.AppendItem(exit_ev)

        # Simulation Menu
        simulationMenu.Append(wx.ID_ANY, '&Run Direct mode')
        simulationMenu.Append(wx.ID_ANY, '&Run Debug mode')
        simulationMenu.Append(wx.ID_ANY, '&Run Step by Step mode')

        # Help Menu
        about_ev = wx.MenuItem(helpMenu, wx.ID_ABOUT, "&About", "Information about this program")
        helpMenu.AppendItem(about_ev)

        "========"
        " Events "
        "========"

        self.Bind(wx.EVT_MENU, self.OnQuit, exit_ev)
        self.Bind(wx.EVT_MENU, self.OnAbout, about_ev)

        # Setting menubar
        self.SetMenuBar(menubar)

        self.splitter = MultiSplitterWindow(self, ID_SPLITTER, style=wx.SP_BORDER)

        colours = ["pink", "yellow", "sky blue", "Lime Green"]
        for colour in colours:
            if(colour == "pink"):
                panel = CPUPanel(self.splitter, colour)
            elif(colour == "yellow"):
                panel = SubSamplePanel(self.splitter, colour)
            else:
                panel = SamplePanel(self.splitter, colour)

            self.splitter.AppendWindow(panel)

        "=============="
        " Window Frame "
        "=============="
        # window frame properties configuration
        displaySize = wx.DisplaySize()
        self.SetSize((displaySize[0] / 1.3, displaySize[1] / 1.3))
        self.SetTitle('Cache Simulator - v0.1 [Alpha]')
        self.Centre()
        self.Show(True)

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "Cache Simulator"
        info.Version = "0.0.1 Beta"
        info.Copyright = "(C) 2015 UC"
        info.WebSite = ("http://www.web.unican.es", "Unican WebSite")
        info.Developers = ["Luis Fernandez Tricio"]
        # Show the wx.AboutBox
        wx.AboutBox(info)

    def OnQuit(self, event):
        self.Close()
        dlg = wx.MessageDialog(self, "Do you really want to close this application?", "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()


def main():

    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
