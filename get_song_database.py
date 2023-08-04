import requests
import os

def DownloadLatest ():
    print ('下载中...')
    url = 'https://raw.githubusercontent.com/Arcaea-Infinity/ArcaeaSongDatabase/main/arcsong.db'
    response = requests.get (url)
    open ('./arcsong.db', 'wb').write (response.content)

if __name__ == '__main__':
    if os.path.exists('./arcsong.db'):
        print ('"arcsong.db" 文件已存在, 将进行覆写')
    DownloadLatest ()
    print ('完成')