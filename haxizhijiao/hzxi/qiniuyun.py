from qiniu import Auth, put_file, etag
import qiniu.config
from django.shortcuts import render
def upload_ren(request):
    return render(request, 'shangchuan.html')

# send to qiniuyun
def upload(request):
    # p_img = request.POST.get('img')
    # p_video = request.POST.get('video')

    #七牛云配置ak、sk、bk_name
    access_key = "CBx0Nvif2WwhNFWDBtZuNdd8Di5lM7LGOq8IJA-U"
    secret_key = "m49-Aj1pMHisMkrL0iKoBKSAfEG7RFeJDKpKZ1DW"
    bucket_name = 'zhijiao'
    q = Auth(access_key, secret_key)
    key = 'pksdg2zat.bkt.clouddn.com'
    #上传文件到七牛后， 七牛将文件名和文件大小回调给业务服务器。
    policy={
     'callbackUrl':'pksdg2zat.bkt.clouddn.com',
     'callbackBody':'filename=$(fname)&filesize=$(fsize)'
     }

    token = q.upload_token(bucket_name, key, 3600, policy)
    return token

    # localfile = '.hzxi/static/img/beijing.jpeg'

    # ret, info = put_file(token, key, localfile)


#  save to local
# coding: utf-8
import os
import time


class Database(object):

    @staticmethod  # 保存静态文件到到本地
    def save_image(file, static_url, middle_url):
        def get_save_time():  # create time to save file
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y%m%d%H%M%S", timeArray)
            return otherStyleTime
        save_time = get_save_time()
        fname = os.path.join(static_url, middle_url, save_time)
        while True:
            if os.path.exists(fname):
                save_time = get_save_time()
                fname = os.path.join(static_url, middle_url, save_time)
            else:
                break
        image_url = os.path.join(middle_url, save_time)
        try:
            with open(fname, 'wb') as pic:
                for c in file.chunks():
                    pic.write(c)
        except:
            os.remove(fname)
            return None #  when create new file failed, return None
        # image size operation
        # im = Image.open(fname)
        # out = im.resize((128, 128), Image.ANTIALIAS)
        # out.save(fname, 'jpeg')
        return image_url

# check file's type
import struct


# 支持文件类型
# 用16进制字符串的目的是可以知道文件头是多少字节
# 各种文件头的长度不一样，少半2字符，长则8字符
def typeList():  # 文件头和类型对应表
    return {
        'FFD8FF': 'JPEG(jpg)',
        '89504E47': 'PNG(png)',
        '47494638': 'GIF(gif)',
        '49492': 'TIFF(tif)'
    }
# 字节码转16进制字符串
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


# 获取文件类型
def filetype(filename):
    binfile = open(filename, 'rb')  # 必需二制字读取
    tl = typeList()
    ftype = 'unknown'
    for hcode in tl.keys():
        numOfBytes = len(hcode) / 2  # 需要读多少字节
        binfile.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
        hbytes = struct.unpack_from("B" * numOfBytes, binfile.read(numOfBytes))  # 一个 "B"表示一个字节
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = tl[hcode]
            break
    binfile.close()
    return ftype


if __name__ == '__main__':
    filetype('file root')