import os
import requests
import configparser
from hashlib import sha1
import hmac
from qiniu import Auth, put_file, etag, urlsafe_base64_encode, BucketManager

# 从配置文件中提取七牛云参数
cf = configparser.ConfigParser()
cf.read(os.path.join(os.path.dirname(__file__), 'confing.ini'))
access_key = cf.get('qiniuyun', 'access_key')
secret_key = cf.get('qiniuyun', 'secret_key')
bucket_name = cf.get('qiniuyun', 'bucket_name')


class Qiniuyun(object):  # 七牛云类，七牛云的操作方法

    @staticmethod
    def delete_qiniuyun(file_url):  # 删除七牛云文件
        q = Auth(access_key, secret_key)
        bucket = BucketManager(q)
        key = file_url
        ret, info = bucket.delete(bucket_name, key)
        if info.status_code == 200:
            print('OK')
            return True
        return False

    @staticmethod
    def save_qiniuyun(root, localfile):  # 保存文件到七牛云
        q = Auth(access_key, secret_key)
        key = root
        policy = {
            'callbackUrl': 'pksdg2zat.bkt.clouddn.com',
            'callbackBody': 'filename=$(fname)&filesize=$(fsize)'
        }
        token = q.upload_token(bucket_name, key, 3600, policy)
        retDate, infoDate = put_file(token, key, localfile)
        return retDate, infoDate

    @staticmethod
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
            return True



if __name__ == '__main__':
    Qiniuyun.delete_qiniuyun('20190109092508')