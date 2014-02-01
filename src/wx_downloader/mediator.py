'''
Created on 1 Feb 2014

@author: Dave
'''

import proxy
from y_mvc import ymvc


class UrlDownloaderMediator(ymvc.Mediator):
    def __init__(self):
        super(UrlDownloaderMediator, self).__init__()
        self.url_download_proxy = proxy.UrlDownloadProxy()

    def on_create_binds(self):
        self.url_download_proxy.bind(self.on_url_added, False)
        self.url_download_proxy.bind(self.on_url_finished, False)
        self.url_download_proxy.bind(self.on_url_stream_detail, False)
        self.url_download_proxy.bind(self.on_error, False)
        self.view.bind(self.on_request_download)

    @ymvc.on_kw_signal
    def on_request_download(self, url, save_to_dir):
        self.url_download_proxy.call.notify_kw(url=url,
            save_to_dir=save_to_dir)

    @ymvc.wx_callafter
    @ymvc.on_attr_signal
    def on_url_added(self, url_added):
        self.gui.add_gauge_panel(url_added)

    @ymvc.wx_callafter
    @ymvc.on_attr_signal
    def on_url_finished(self, url_finished):
        self.gui.remove_gauge_panel(url_finished)

    @ymvc.wx_callafter
    @ymvc.on_attr_signal
    def on_url_stream_detail(self, url_stream_detail):
        url, percentage = url_stream_detail.url, url_stream_detail.percentage
        self.gui.set_url_gauge(url, percentage)

    @ymvc.wx_callafter
    @ymvc.on_attr_signal
    def on_error(self, error):
        self.gui.message_dialog(*error)
