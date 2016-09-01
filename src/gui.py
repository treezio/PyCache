#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from wx import AboutBox
from wx.lib.splitter import MultiSplitterWindow
import os
import sys


ID_SPLITTER = 300


class CacheGUI(wx.Frame):

    def __init__(self, module):
        super(CacheGUI, self).__init__(None, wx.ID_ANY)

        self.InitUI(module)

    def InitUI(self, module):

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
        direct_ev = simulationMenu.Append(wx.ID_ANY, '&Run Direct mode')
        simulationMenu.Append(wx.ID_ANY, '&Run Debug mode')
        step_ev = simulationMenu.Append(wx.ID_ANY, '&Run one step')

        # Help Menu
        about_ev = wx.MenuItem(helpMenu, wx.ID_ABOUT, "&About", "Information about this program")
        helpMenu.AppendItem(about_ev)

        "========"
        " Events "
        "========"

        self.Bind(wx.EVT_MENU, self.OnQuit, exit_ev)
        self.Bind(wx.EVT_MENU, self.OnAbout, about_ev)
        self.Bind(wx.EVT_MENU, self.OnDirectMode, direct_ev)
        self.Bind(wx.EVT_MENU, self.OnStep, step_ev)

        # Setting menubar
        self.SetMenuBar(menubar)

        self.splitter = MultiSplitterWindow(self, ID_SPLITTER, style=wx.SP_BORDER)
        self.cpu_module = module
        self.splitter.AppendWindow(module.make_viewer(self.splitter))
        while module.has_next():
            module = module.up
            self.splitter.AppendWindow(module.make_viewer(self.splitter))

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
        dlg = wx.MessageDialog(self, "Do you really want to close this application?", "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnStep(self, event):
        print "Ejecución de un paso"
        if self.cpu_module.finished():
            return
        while not self.cpu_module.exe():
            1
        print "End"

    def OnDirectMode(self, event):
        print "Ejecución continua GUI"
        self.cpu_module.reset()
        while not self.cpu_module.finished():
            while not self.cpu_module.exe():
                1
        print "End"


def main(module):
    ex = wx.App()
    CacheGUI(module)
    ex.MainLoop()

if __name__ == '__main__':
    main()
