# -*- coding: utf-8 -*-

import os
from . import haxi_timechange
from haxizhijiao import settings


class File_Operation(object):

    @staticmethod
    def save_file(file, static_url=settings.MEDIA_ROOT):  # 保存文件在本地
        save_time = haxi_timechange.ChangeTime.change_time_to_date("%Y%m%d%H%M%S")
        fname = os.path.join(static_url, save_time + file.name)
        while True:
            if os.path.exists(fname):
                save_time = haxi_timechange.ChangeTime.change_time_to_date("%Y%m%d%H%M%S")
                fname = os.path.join(static_url, save_time + file.name)
            else:
                break
        image_url = save_time + file.name
        try:
            with open(fname, 'wb') as pic:
                for c in file.chunks():
                    pic.write(c)
        except:
            if os.path.exists(fname):
                os.remove(fname)
            return None  # when create new file failed, return None
        return image_url