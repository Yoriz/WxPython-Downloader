'''
Created on 31 Jan 2014

@author: Dave
'''

import requests
import os
import collections


class FileStreamDetails(collections.namedtuple('FileStreamDetails',
        ('url', 'file_size', 'bytes_dl'))):
    __slots__ = ()

    @property
    def file_name(self):
        return os.path.basename(self.url)

    @property
    def percentage(self):
        return (self.bytes_dl / (self.file_size + 0.0)) * 100

    def __str__(self):
        return 'FileStreamDetails <url: {}, %: {}>'.format(
            self.url, self.percentage)


def stream_download(url, save_to_dir):
    file_name = os.path.basename(url)
    save_to_path = os.path.join(save_to_dir, file_name)

    header = requests.head(url)
    fsize = int(header.headers["content-length"]) / 1024

    req = requests.get(url, stream=True)
    bytes_dl = 0
    with open(save_to_path, "wb") as fh:
        for byte in req.iter_content(chunk_size=1024):
            if byte:
                fh.write(byte)
                fh.flush()
            bytes_dl += 1024
            if bytes_dl < fsize:
                yield FileStreamDetails(url, fsize, bytes_dl)

    print "DONE!"
    yield FileStreamDetails(url, fsize, fsize)
