import os

def ask_startfile (file_path):
    print ('是否打开文件?')
    print ('[0] 不打开; [1] 打开')
    do_startfile = input ('input: ')
    print ()
    if (do_startfile == '1'):
        os.startfile (file_path)
        print ('已启动文件')

def best30_print (potential_list):
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

def best30_txt (potential_list, best30, max_ptt):
    with open ('./Best30.txt', 'w', encoding = 'utf-8-sig') as txt_file:
        txt_file.write (f'Best 30 AVG: {best30:.8f}\n')
        txt_file.write (f'Maximum PTT: {max_ptt:.8f}\n\n')
        for i in range(30):
            txt_file.write (f'#{i+1}: {potential_list[i][1]}\n')
            txt_file.write (f'难度: {potential_list[i][2]}\n')
            txt_file.write (f'定数: {potential_list[i][3]}\n')
            txt_file.write (f'分数: {potential_list[i][4]}\n')
            txt_file.write (f'潜力值: {potential_list[i][0]:.8f}\n')
            txt_file.write (f'PURE: {potential_list[i][6]} (+{potential_list[i][5]})\n')
            txt_file.write (f'FAR:  {potential_list[i][7]}\n')
            txt_file.write (f'LOST: {potential_list[i][8]}\n')
            txt_file.write ('\n')
    output_path = os.path.join (os.getcwd (), 'Best30.txt')
    print (f'已输出到"{output_path}"')
    print ()
    ask_startfile (output_path)

def best30_csv (potential_list):
    with open('./Best30.csv', 'w', encoding = 'utf-8-sig') as csv_file:
        csv_file.write (f'#, 乐曲名, 难度, 定数, 分数, 潜力值, PURE, FAR, LOST\n')
        for i in range(30):
            csv_file.write (f'{i+1},"{potential_list[i][1]}",{potential_list[i][2]},{potential_list[i][3]},{potential_list[i][4]},{potential_list[i][0]:.8f},{potential_list[i][6]} (+{potential_list[i][5]}),{potential_list[i][7]},{potential_list[i][8]}\n')
    output_path = os.path.join (os.getcwd (), 'Best30.csv')
    print (f'已输出到"{output_path}"')
    print ()
    ask_startfile (output_path)