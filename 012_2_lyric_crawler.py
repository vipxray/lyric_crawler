# Author: Haorui Chen
# Update: Sept 22

from bs4 import BeautifulSoup
import requests
import time
import random
import traceback

# switchs:
is_verbose = 0
is_log = 1

# dictionaries:
url_title_search_link = 'http://www.lyricsplanet.com/search.php?field=title&value='
aphlpabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
tmp_title_list = ['A', 'B', 'C']
# the list of last page according to thee alphbat_list
# already found and stored from website
lp_list = [32,34,31,30,13,22,21,28,52,9,6,35,30,18,17,20,2,18,62,64,6,4,38,1,14,1]
headers = {
    'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'dealer.m.yiche.com',
    'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.36'
}


# Veriables

# input lyric id list file
old_file_name = 'lyric_id.txt'

# old file name's data simplfied into the file below.
file_name = 'id_list_cleaned_data.txt'

# id list from the txt file
id_list = []

# current line id list
id_list_cl = []

# random waiting time:
waitTime1 = 5
waitTime2 = 0.5
waitTime_c = 0
# wt = random.random() * waitTime

# data starting point6
# TODO: \\continue from #584
idx_start = 552
# TO 559


# Functions:
def getID(fName):
    try:
        tmp_id_list = []
        tmp_line = []
        f_id_list = open(fName, 'r+')
        ln_1 = f_id_list.readline()
        while ln_1:
            # TODO: process current line to get pageNumber and lyricID
            tmp_line = ln_1.split(',')
            tmp_id_list.append(tmp_line)
            ln_1 = f_id_list.readline()
        f_id_list.close()
        # got all id in hte tmp_id_list
        return tmp_id_list
    except:
        print('Exception: getID()')

def clean_data_file(fName):
    f_id_list = open(fName, 'r+')
    f_op = open('id_list_cleaned_data.txt', 'w+')
    ln1 = f_id_list.readline()
    while ln1:
        # print(type(ln1))
        print(ln1)
        ln1 = ln1.replace('\'', '').replace(' ', '')
        ln1 = str(ln1[1:len(ln1)-2])
        tmp_ln = str(ln1) + '\n'
        print(ln1)
        print('============')
        f_op.writelines(tmp_ln)
        ln1 = f_id_list.readline()
    f_id_list.close()
    f_op.close()

def print_data(list_id):
    for lid in list_id:
        print(lid)

def obtain_data(id_list_od):
    cur_lyric_pkg = []
    print('Obtaining data')
    idx_tst = 0
    idx_idc = 0
    for lid in id_list_od:
        if idx_idc < idx_start:
            idx_idc += 1
            # print(idx_idc)
        else:
            xl_0 = str(lid[0])
            x_0 = xl_0[len(xl_0)-1:len(xl_0)]
            xl_1 = str(lid[1])
            x_1 = xl_1[len(xl_1)-1:len(xl_1)]
            if x_0 == 'Y':
                if x_1 == '7' or x_1 == '8' or x_1 == '9':
                    idx_idc += 1
                    try:
                        waitTime_plus = waitTime_c * random.random()
                        fileN = '09' + str(idx_idc) + '_lyric_data_package.txt'
                        # print(fileN)
                        fx = open(fileN, 'w+')
                    except:
                        print('Open file ERROR')
                    if is_log:
                        print('Retrieving data: ' + lid[0] + ', ' + lid[1] + ', (' + str(idx_idc) + '/607)')
                    wt1 = waitTime1 * random.random()
                    time.sleep(wt1)
                    tmp_ln2 = lid[0] + ',' + lid[1] + '\n'
                    try:
                        fx.writelines(str(tmp_ln2))
                    except:
                        print('FileName Writeline ERROR')
                    for id_idx in range(2, len(lid)):
                        tmp_link = 'http://www.lyricsplanet.com/lyrics.php?id=' + lid[id_idx]
                        cur_lyric_pkg = get_single_lyric_info(tmp_link)
                        tmp_ln1 = str(cur_lyric_pkg) + '\n'
                        try:
                            fx.writelines(tmp_ln1)
                            if is_log:
                                print('\t>>\'' + str(cur_lyric_pkg[1]) + '\' ,gathered.')
                                if is_verbose:
                                    print(tmp_link)
                                    print(cur_lyric_pkg)
                                    print(tmp_ln1)
                        except:
                            print('Lyric Writeline ERROR')
                        # wait random time to open the link
                        wt2 = random.random() * waitTime2 + waitTime_plus
                        time.sleep(wt2)
                        # idx_tst += 1
                        # if idx_tst > 3:
                    #     break
                    # break
                    # idx_tst += 1
                    # if idx_tst > 3:
                    #     break
                    fx.close()

        ###############################################################################################
        # else:
        #     idx_idc += 1
        #     try:
        #         waitTime_plus = waitTime_c * random.random()
        #         fileN = '09' + str(idx_idc) + '_lyric_data_package.txt'
        #         # print(fileN)
        #         fx = open(fileN, 'w+')
        #     except:
        #         print('Open file ERROR')
        #     if is_log:
        #         print('Retrieving data: ' + lid[0] + ', ' + lid[1] + ', (' + str(idx_idc) + '/607)')
        #     wt1 = waitTime1 * random.random()
        #     time.sleep(wt1)
        #     tmp_ln2 = lid[0] + ',' + lid[1] + '\n'
        #     try:
        #         fx.writelines(str(tmp_ln2))
        #     except:
        #         print('FileName Writeline ERROR')
        #     for id_idx in range(2, len(lid)):
        #         tmp_link = 'http://www.lyricsplanet.com/lyrics.php?id=' + lid[id_idx]
        #         cur_lyric_pkg = get_single_lyric_info(tmp_link)
        #         tmp_ln1 = str(cur_lyric_pkg) + '\n'
        #         try:
        #             fx.writelines(tmp_ln1)
        #             if is_log:
        #                 print('\t>>\'' + str(cur_lyric_pkg[1]) + '\' ,gathered.')
        #                 if is_verbose:
        #                     print(tmp_link)
        #                     print(cur_lyric_pkg)
        #                     print(tmp_ln1)
        #         except:
        #             print('Lyric Writeline ERROR')
        #         # wait random time to open the link
        #         wt2 = random.random() * waitTime2 + waitTime_plus
        #         time.sleep(wt2)
        #         # idx_tst += 1
        #         # if idx_tst > 3:
        #     #     break
        #     # break
        #     # idx_tst += 1
        #     # if idx_tst > 3:
        #     #     break
        #     fx.close()
        ###############################################################################################


def get_single_lyric_info(tmp_link):
    try:
        this_lyric_data = []
        homepage_html = requests.get(tmp_link, headers)
        soup = BeautifulSoup(homepage_html.content, "lxml")
        data_1 = soup.find_all("div", {"id": "lyrics"})
        for d1 in data_1:
            h2_tags = d1.find_all('h2')
            this_lyric_data.append(h2_tags[0].text)
            this_lyric_data.append(h2_tags[1].text)
            p_tags = d1.find_all('p')
            this_lyric_data.append(p_tags[1].text)
            if is_verbose:
                print(h2_tags[0])
                print('===')
                print(h2_tags[1])
                print('===')
                print(p_tags[1].text)
                # print(data_1)
        # return a list with author and name of the song and lyrics
        return this_lyric_data
    except:
        print('Exception: get_single_lyric_info()')


# Main #

# clean data: (DONE)
#clean_data_file(old_file_name)

# get lyric's id from local index file
id_list = getID(file_name)

# check if data is complete
#print_data(id_list)

# retrive data using the id
obtain_data(id_list)
