import os
import time
from django.http import JsonResponse
from django.shortcuts import render
from qiniu import Auth, put_file, etag
from . import models
from haxizhijiao import settings


def save_image(file, static_url=settings.MEDIA_ROOT):
    def get_save_time():  # create time to save file
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y%m%d%H%M%S", timeArray)
        return otherStyleTime

    save_time = get_save_time()
    fname = os.path.join(static_url, save_time+file.name)
    while True:
        if os.path.exists(fname):
            save_time = get_save_time()
            fname = os.path.join(static_url, save_time+file.name)
        else:
            break
    image_url = save_time+file.name
    try:
        with open(fname, 'wb') as pic:
            for c in file.chunks():
                pic.write(c)
    except:
        os.remove(fname) if os.path.exists(fname) else None
        return None  # when create new file failed, return None
    # image size operation
    # im = Image.open(fname)
    # out = im.resize((128, 128), Image.ANTIALIAS)
    # out.save(fname, 'jpeg')
    return image_url

def ceshi(request):
    return render(request, 'chuanm.html')


def parseRet(retData, respInfo):
    if retData != None:
        print("Upload file success!")
        print("Hash: " + retData["hash"])
        print("Key: " + retData["key"])

        # 检查扩展参数
        for k, v in retData.items():
            if k[:2] == "x:":
                print(k + ":" + v)

        # 检查其他参数
        for k, v in retData.items():
            if k[:2] == "x:" or k == "hash" or k == "key":
                continue
            else:
                print(k + ":" + str(v))
    else:
        print("Upload file failed!")
        print("Error: " + respInfo.text_body)


def upload(request):
    if request.method == 'POST':
        # name = request.POST.get('username')
        data = []
        resp = []
        for i in range(1,11):
            name = 'img{0}'.format(i)
            avatar = request.FILES.get(name)
            if not avatar:
                return JsonResponse({'msg': resp})
            root = save_image(avatar) # 文件的相对路径
            if root:
                localfile = os.path.join(settings.MEDIA_ROOT, root)
                data.append(root)
            uuid = root
            models.Userp.objects.create(avatar=root)
            access_key = "CBx0Nvif2WwhNFWDBtZuNdd8Di5lM7LGOq8IJA-U"
            secret_key = "m49-Aj1pMHisMkrL0iKoBKSAfEG7RFeJDKpKZ1DW"
            bucket_name = 'zhijiao'
            q = Auth(access_key, secret_key)
            print(root)
            key = root
            print(key)
            policy = {
                'callbackUrl': 'pksdg2zat.bkt.clouddn.com',
                'callbackBody': 'filename=$(fname)&filesize=$(fsize)'
            }
            token = q.upload_token(bucket_name, key, 3600, policy)
            # localfile = './static/uploads/avatar/%s' % avatar
            retDate, infoDate = put_file(token, key, localfile)
            print(root)
            print(localfile)
            parseRet(retDate, infoDate)
            # os.remove(localfile)
            resp.append({
                'url': 'http://pksdg2zat.bkt.clouddn.com' + '/' + root
            })
        return JsonResponse(data={'msg': 'OK'})

    # return render(request, 'upload.html')

# STATIC_URL = '/static/'
#
# MEDIA_ROOT = os.path.join(BASE_DIR, 'static/uploads')
#
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]