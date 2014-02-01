'''
Created on 31 Jan 2014

@author: Dave
'''

import file_downloader
from y_mvc import ymvc


class UrlDownloadProxy(ymvc.Proxy):
    url_added = None
    url_finished = None
    url_stream_detail = None
    error = None

    def __init__(self):
        super(UrlDownloadProxy, self).__init__()
        self.add_obs_attrs('url_added', 'url_finished',
            'url_stream_detail', 'error')

        self.call.bind(self.on_download_url)

    @ymvc.on_kw_signal
    def on_download_url(self, url, save_to_dir):
        self.download_url(url, save_to_dir)

    @ymvc.run_async
    def download_url(self, url, save_to_dir):
        self.url_added = url
        try:
            for url_stream_detail in file_downloader.stream_download(url,
                    save_to_dir):
                self.url_stream_detail = url_stream_detail
        except Exception as exception:
            self.error = ('Download error!', str(exception))
        finally:
            self.url_finished = url
