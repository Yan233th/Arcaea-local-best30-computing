import sqlite3
import bisect
from tkinter import filedialog
import os
import sys

import get_song_database


def custom_sort (x):
    return x[0] * (-1)

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

def output_best30 (potential_list):
    with open('./Best30.txt', 'w') as file:
        file.write (f'Best 30 AVG: {best30:.8f}\n')
        file.write (f'Maximum PTT: {max_ptt:.8f}\n\n')
        for i in range(30):
            file.write (f'#{i+1}: {potential_list[i][1]}\n')
            file.write (f'难度: {potential_list[i][2]}\n')
            file.write (f'定数: {potential_list[i][3]}\n')
            file.write (f'分数: {potential_list[i][4]}\n')
            file.write (f'潜力值: {potential_list[i][0]:.8f}\n')
            file.write (f'PURE: {potential_list[i][6]} (+{potential_list[i][5]})\n')
            file.write (f'FAR:  {potential_list[i][7]}\n')
            file.write (f'LOST: {potential_list[i][8]}\n')
            file.write('\n')
    output_path = os.path.join (os.getcwd (), 'Best30.txt')
    print (f'已输出到"{output_path}"')
    print ()
    os.startfile (output_path)

def print_best30 (potential_list):

    for i in range (30):
        print (f'#{i+1}: {potential_list[i][1]}')
        print (f'难度: {potential_list[i][2]}')
        print (f'定数: {potential_list[i][3]}')
        print (f'分数: {potential_list[i][4]}')
        print (f'潜力值: {potential_list[i][0]:.8f}')
        print (f'PURE: {potential_list[i][6]} (+{potential_list[i][5]})')
        print (f'FAR:  {potential_list[i][7]}')
        print (f'LOST: {potential_list[i][8]}')
        print ()
    print ('[0] 退出程序; [1] 输出到txt文件中')
    do_output_best30 = input ('input: ')
    print ()
    if (do_output_best30 == '1'):
        output_best30 (potential_list)


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
    print ('[0] 退出程序; [1] 输出完整Best30')
    do_print_best30 = input ('input: ')
    print ()
    if (do_print_best30 == '1'):
        print_best30 (potential_list)

    close_all ()