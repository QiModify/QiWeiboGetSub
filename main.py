#
#  main.py
#  QiiWeiboGetSub
#
#  Created by QiModify on 2022/9/18.
#
import json
import time

import requests


def getSub():
    qrcodeUrl = 'https://login.sina.com.cn/sso/qrcode/image?entry=weibo&size=180&callback=JSON'
    header = {
        'Referer': 'https://weibo.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    response = json.loads(
        requests.get(url=qrcodeUrl, headers=header).text.replace('window.JSON && JSON(', '').replace(');', ''))
    imgUrl = 'https:' + response['data']['image']
    qrId = response['data']['qrid']
    res = requests.get(url=imgUrl, headers=header).content
    timeStamp = str(int(time.time()))
    with open(f'{timeStamp}.png', 'wb+') as f:
        f.write(res)

    while True:
        checkUrl = f'https://login.sina.com.cn/sso/qrcode/check?entry=weibo&qrid={qrId}&callback=JSON'
        response = json.loads(
            requests.get(url=checkUrl, headers=header).text.replace('window.JSON && JSON(', '').replace(');', ''))
        if response['msg'] != 'succ':
            print("叼毛扫码快点")
            time.sleep(3)
            continue
        else:
            alt = response['data']['alt']
            url = f'https://login.sina.com.cn/sso/login.php?entry=weibo&returntype=TEXT&crossdomain=1&cdult=3&domain=weibo.cn&alt={alt}&savestate=30&callback=JSON'
            res = json.loads(
                requests.get(url=url, headers=header).text.replace('JSON(', '').replace(');', '')
            )
            print(res)
            crossDomainUrlList = res['crossDomainUrlList']
            for i in crossDomainUrlList:
                if 'https://passport.weibo.cn/sso/crossdomain?service=sinawap' in i:
                    loginUrl = i
            loginRes = requests.get(url=loginUrl, headers=header).headers
            cookie = loginRes['Set-Cookie'].split(';')
            for ck in cookie:
                if "SUB" in ck[:10]:
                    sub = ck
                    print("已获取到SUB")
                    print(sub)
                else:
                    print('未获取到SUB')
            break


if __name__ == '__main__':
    getSub()
