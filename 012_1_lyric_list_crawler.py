# Author: Haorui Chen
# Update: Aug 26

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

# variables:
# wait time in between (0,15) seconds
wait_time = 10
lyric_id_list_list = []


# FUNCTION:

# get the last_page number of each search of each starting letter
def get_last_page(start_letter):
    tmp_link = url_title_search_link + start_letter
    if is_log:
        print('//crawling the link of lyrics\'s title start with', start_letter)
    homepage_html = requests.get(tmp_link, headers)
    if is_log:
        print('//Website package required successfully.')
        if is_verbose:
            print(homepage_html.headers)
    soup = BeautifulSoup(homepage_html.content, "lxml")
    if is_verbose:
        print(soup)
    # find the last page and loop all the page of lyric starting with current searching letter
    tmp_page_text_list = soup.find_all('strong')
    tmp_page_text =str(tmp_page_text_list[4])
    page_idx_end = tmp_page_text.find('</')
    last_page = tmp_page_text[8:page_idx_end]
    if is_log:
        print('//Got the last page number', last_page)
        if is_verbose:
            print(tmp_page_text)
            print(last_page)





    # find all link for lyric in current page
    # a_list = soup.find_all('a')
    # for alink in a_list:
    #     a_chk = str(alink)
    #     if '?id=' in a_chk:
    #         print(alink)
    return last_page


# find all last pages according to the lyric starting letter search
def get_all_last_page(aphlpabet_list):
    f1 = open('012_lastPageNumber_list.txt', 'w+')
    for al in aphlpabet_list:
        lp_tmp = get_last_page(al)
        lp_list.append(lp_tmp)
        wLine1 = lp_tmp + ','
        f1.write(wLine1)
    f1.close
    if is_log:
        print('//all last page data found.')
        if is_verbose:
            print('last_page_list:')
            for l in lp_list:
                print(l)


# find all lyrics id in current page:
def get_lyric_id(lt, p_idx, wait_time):
    id_list_tmp0 = []
    idx_str = 'START_LETTER:' + lt + ',PAGE_NUMBER_#' + str(p_idx)
    id_list_tmp0.append(idx_str)
    tmp_link = url_title_search_link + lt + '&p=' + str(p_idx)
    # wait random time to avoid ip band.
    wt = random.random() * wait_time
    print('...wait time:' + str(wt))
    time.sleep(wt)
    # Request all the link we have
    homepage_html = requests.get(tmp_link, headers)
    soup = BeautifulSoup(homepage_html.content, "lxml")
    #print(soup.table)
    # grep all id out of soup
    id_text = soup.find_all('td')
    for idt in id_text:
        tmp_id_line = str(idt.find('a'))
        id_idx1 = tmp_id_line.find('id=')
        id_idx2 = tmp_id_line.find('">')
        tmp_id = tmp_id_line[id_idx1+3:id_idx2]
        id_list_tmp0.append(tmp_id)
    if is_log:
        #print('//all lyrics\' in current page retrieved.')
        print('//Open letter:' + tmp_link + ' Page: ' + str(p_idx))
        if is_verbose:
            print(tmp_id_line[0:id_idx2])
            print(tmp_id)
    return id_list_tmp0


# Assumby all data we have to a link
# open the link to get the
def get_all_lyric_id(alphabet_list):
    # Find all lyric id and store them into the text file
    f2 = open('013_all_lyric_id.txt', 'w+')
    # By alphabet, then by page form 1-last_page
    for i in range (0,26):
    # for test
    # for i in range(0, 2):
        # wait random time to avoid ip band.
        wt = random.random() * wait_time
        print('...wait time:' + str(wt))
        time.sleep(wt)
        letter_t = aphlpabet_list[i]
        max_page = lp_list[i]
        if is_log:
            print('//search with starting letter:', letter_t)
        for page_idx in range(0,max_page):
        # for test
        #for page_idx in range(0, 2):
            # get all lyrics id form current page
            # this list store page by page. each entry including all list in the current page.
            lyric_id_list_list.append(get_lyric_id(letter_t, page_idx, wt))
    f3 = open('014_lyric_id.txt', 'w+')
    for f in lyric_id_list_list:
        print(f)
        line_tmp = str(f) + '\n'
        f3.writelines(line_tmp)
    f3.close()






# MAIN
# try:
#     get_link()
# except:
#     print('get_link() failed!')
#     print()
print('getting all lyric start with letter', tmp_title_list[0])

# DON'T NEED THIS FUNCTION ANYMORE
# SINCE WE ALREADY ACQUIRED THE DATA
#get_all_last_page(alphabet_list)

#get_all_lyric_id(alphabet_list)
get_all_lyric_id(tmp_title_list)


#tl = 'http://www.lyricsplanet.com/search.php?field=title&value=B&p=2'
#get_lyric_id(tl, wait_time)
