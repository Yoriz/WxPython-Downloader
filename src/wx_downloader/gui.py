'''
Created on 31 Jan 2014

@author: Dave
'''

import os

import wx
from wx.lib import sized_controls, newevent, scrolledpanel


UrlDownloadEvent, EVT_URL_DOWNLOAD = newevent.NewCommandEvent()


def message_dialog(parent, title_text, error_text, icon=None):
    if not icon:
        icon = wx.ICON_ERROR
    elif icon == 'information':
        icon = wx.ICON_INFORMATION
    dialog = wx.MessageDialog(parent, error_text, title_text,
                              icon | wx.OK | wx.CENTER)
    dialog.ShowModal()
    dialog.Destroy()


class GaugePanel(sized_controls.SizedPanel):
    def __init__(self, url, *args, **kwargs):
        super(GaugePanel, self).__init__(*args, **kwargs)
        self.SetExtraStyle(wx.TAB_TRAVERSAL)

        lbl = wx.StaticText(self, label=url)
        lbl.SetSizerProps(border=(('left',), 1))
        self.gauge = wx.Gauge(self)
#         self.gauge.SetRange(1)
        self.gauge.SetSizerProps(border=(('left', 'right', 'bottom'), 5),
            expand=True)

    def set_gauge(self, percentage):
        self.gauge.SetValue(percentage)


class MyPanel(scrolledpanel.ScrolledPanel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        super(MyPanel, self).__init__(*args, **kwargs)
        self.url_gauges = {}

        # create the sizers
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        dl_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # create the widgets
        lbl = wx.StaticText(self, label="Download URL:")
        self.dl_txt = wx.TextCtrl(self)
        btn = wx.Button(self, label="Download")
        btn.Bind(wx.EVT_BUTTON, self.onDownload)

        # layout the widgets
        dl_sizer.Add(lbl, 0, wx.ALL | wx.CENTER, 5)
        dl_sizer.Add(self.dl_txt, 1, wx.EXPAND | wx.ALL, 5)
        dl_sizer.Add(btn, 0, wx.ALL, 5)
        self.main_sizer.Add(dl_sizer, 0, wx.EXPAND)

        self.SetSizer(self.main_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def add_gauge_panel(self, url):
        gauge_panel = GaugePanel(url, self, style=wx.BORDER_SIMPLE)
        self.main_sizer.Insert(1, gauge_panel, 0, wx.ALL | wx.EXPAND, 5)
        self.Layout()
        self.url_gauges[url] = gauge_panel

    def remove_gauge_panel(self, url):
        gauge_panel = self.url_gauges.pop(url)
        self.main_sizer.Detach(gauge_panel)
        gauge_panel.Destroy()
        self.Layout()

    def set_url_gauge(self, url, percentage):
        self.url_gauges[url].set_gauge(percentage)

    #----------------------------------------------------------------------
    def onDownload(self, event):
        """
        Update display with downloading gauges
        """
        url = self.dl_txt.GetValue()
        if self.url_gauges.get(url):
            error_text = '{}\n is already downloading'.format(url)
            message_dialog(self, 'URL Error!', error_text)
        else:
            evt = UrlDownloadEvent(self.Id, url=url,
                save_to_dir=os.getcwd())
            wx.PostEvent(self, evt)


########################################################################
class DownloaderFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Downloader", size=(800, 400))
        self.panel = MyPanel(self)
        self.Show()

    def add_gauge_panel(self, url):
        self.panel.add_gauge_panel(url)

    def set_url_gauge(self, url, percentage):
        self.panel.set_url_gauge(url, percentage)

    def remove_gauge_panel(self, url):
        self.panel.remove_gauge_panel(url)

    def message_dialog(self, title_text, error_text):
        message_dialog(self, title_text, error_text)


#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = DownloaderFrame()
    frame.add_gauge_panel('Test1')
    frame.add_gauge_panel('Test2')
    frame.add_gauge_panel('Test3')
    frame.set_url_gauge('Test3', 50)
    frame.remove_gauge_panel('Test2')
    app.MainLoop()
