'''
Created on 1 Feb 2014

@author: Dave
'''


import wx

import gui
import mediator
from y_mvc import ymvc


class WxDownloader(gui.DownloaderFrame):
    def __init__(self, *args, **kwargs):
        super(WxDownloader, self).__init__(*args, **kwargs)
        self.view = ymvc.View(self)
        self.Bind(gui.EVT_URL_DOWNLOAD, self.on_url_download)

    def on_url_download(self, event):
        url, save_to_dir = event.url, event.save_to_dir
        self.view.notify_kw(url=url, save_to_dir=save_to_dir)

if __name__ == '__main__':
    wxapp = wx.App(False)
    wx_downloader = WxDownloader()
    wx_downloader.Show()
    wx_downloader.view.set_mediator(mediator.UrlDownloaderMediator())
    wxapp.MainLoop()
