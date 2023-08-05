import sqlite3
import bisect
from tkinter import filedialog
import os
import sys

import get_song_database
import output


def custom_sort (value):
    return value[0] * (-1)

def close_all ():
    data_cursor.close ()
    data_sql.close ()
    score_cursor.close ()
    score_sql.close ()

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
    if not os.path.exists ('./arcsong.db'):
        print ('不存在 "arcsong.db" 文件, 将进行下载')
        get_song_database.DownloadLatest ()
    data_sql = sqlite3.connect ('./arcsong.db')
    data_cursor = data_sql.cursor ()

    score_cursor.execute ('SELECT songId, songDifficulty, score, shinyPerfectCount, perfectCount, nearCount, missCount FROM scores')
    score_list = score_cursor.fetchall ()
    potential_list = []
    difficulty_name = ['PAST', 'PRESENT', 'FUTURE', 'BEYOND']
    for song_id, song_difficulty, score, critical_pure, pure, far, lost in score_list:
        data_cursor.execute (f'SELECT rating, name_en, name_jp FROM charts WHERE song_id = "{song_id}" and rating_class = {song_difficulty}')
        result = (data_cursor.fetchall ())
        rating = result[0][0] / 10
        if result[0][2] == '':
            song_name = result[0][1]
        else:
            song_name = result[0][1] + ' | ' + result[0][2]
        potential = potential_compute (score, rating)
        bisect.insort (potential_list, [potential, song_name, difficulty_name[song_difficulty], rating, score, critical_pure, pure, far, lost], key = custom_sort)

    if (len (potential_list) < 30):
        print ()
        print ('你好像还没有打到30首歌哦')
        print ()
        close_all ()
        sys.exit ()
    best30 = 0
    max_r10 = 0
    for i in range (30):
        best30 += potential_list[i][0]
    for i in range (10):
        max_r10 += potential_list[i][0]
    max_ptt = (best30 + max_r10) / 40
    best30 /= 30
    print ()
    print (f'Best 30 AVG: {best30:.8f}')
    print (f'Maximum PTT: {max_ptt:.8f}')
    print ()
    while (True):
        print ('选择操作:')
        print ('[0] 退出程序; [1] 输出完整Best30到终端; [2] 输出完整Best30到txt; [3] 输出完整Best30到csv')
        output_content = input ('input: ')
        print ()
        match output_content:
            case '0':
                break
            case '1':
                output.best30_print (potential_list)
            case '2':
                output.best30_txt (potential_list, best30, max_ptt)
            case '3':
                output.best30_csv (potential_list)
            case _:
                print ('输入值无效, 请重新输入')
                print ()

    close_all ()