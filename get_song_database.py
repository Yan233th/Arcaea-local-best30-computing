import requests
import os

def DownloadLatest ():
    print ('下载中...')
    url = 'https://raw.gitmirror.com/Arcaea-Infinity/ArcaeaSongDatabase/main/arcsong.db'
    response = requests.get (url)
    open ('./arcsong.db', 'wb').write (response.content)
    print ('下载完成')

if __name__ == '__main__':
    if os.path.exists('./arcsong.db'):
        print ('"arcsong.db" 文件已存在, 将进行覆写')
    DownloadLatest ()