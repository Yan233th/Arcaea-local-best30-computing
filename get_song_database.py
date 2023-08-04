import requests
import os

def DownloadLatest ():
    url = 'https://raw.githubusercontent.com/Arcaea-Infinity/ArcaeaSongDatabase/main/arcsong.db'
    response = requests.get (url)
    open ('./arcsong.db', 'wb').write (response.content)

if __name__ == '__main__':
    if os.path.exists('./arcsong.db'):
        print ('"arcsong.db" 文件已存在, 将进行覆写')
    DownloadLatest ()