import sqlite3
import bisect
from tkinter import filedialog
import os

import get_song_database

difficulty_name = ['PAST', 'PRESENT', 'FUTURE', 'BEYOND']

def custom_sort (x):
    return x[0] * (-1)

def potential_compute (score, chart_constant):
    if (score < 9800000):
        potential = chart_constant + (score-9500000) / 300000
        if potential > 0:
            return potential
        else:
            return 0
    elif (score >= 10000000):
        return chart_constant + 2
    else:
        return chart_constant + 1 + (score-9800000) / 200000

if __name__ == '__main__':
    print ('请选择存有Arcaea本地游戏成绩的st3文件')
    score_path = filedialog.askopenfilename ()
    score_sql = sqlite3.connect (score_path)
    score_cursor = score_sql.cursor ()
    if not os.path.exists('./arcsong.db'):
        print ('不存在 "arcsong.db" 文件, 将进行下载')
        get_song_database.DownloadLatest ()
    data_sql = sqlite3.connect ('./arcsong.db')
    data_cursor = data_sql.cursor ()
    score_cursor.execute ('SELECT songId, songDifficulty, score FROM scores')
    score_list = score_cursor.fetchall ()
    potential_list = []
    for song_id, song_difficulty, score in score_list:
        data_cursor.execute (f'SELECT rating, name_en FROM charts WHERE song_id = "{song_id}" and rating_class = {song_difficulty}')
        result = (data_cursor.fetchall ())
        rating = result[0][0] / 10
        song_name = result[0][1]
        potential = potential_compute (score, rating)
        bisect.insort (potential_list, (potential, song_name, rating, score, difficulty_name[song_difficulty]), key=custom_sort)
    Best30 = 0
    for i in range(30):
        Best30 += potential_list[i][0]
    Best30 /= 30
    print ()
    print (f'你的Best30为: {Best30}')
    print ()
    print ('[0] 退出程序; [1] 输出完整Best30')
    action = input ('input: ')
    print ()
    if (action == '1'):
        for i in range(30):
            print (f'歌曲名称: {potential_list[i][1]}')
            print (f'定数: {potential_list[i][2]}')
            print (f'难度: {potential_list[i][3]}')
            print (f'潜力值: {potential_list[i][0]}')
            print ()

    data_cursor.close ()
    data_sql.close ()
    score_cursor.close ()
    score_sql.close ()
