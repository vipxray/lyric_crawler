from bs4 import BeautifulSoup
import requests
import time
import random
import traceback

is_verbose = 0
is_log = 1


# sotring list

#browser = webdriver.Firefox()#Chrome('./chromedriver.exe')
url_hp = 'http://www.lyricsplanet.com/'
url_hp_link = 'http://www.lyricsplanet.com/links.php'

headers = {
    'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'dealer.m.yiche.com',
    'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.36'
}


def get_web_list():
    # send a request to the target website
    # and store the response into the homepage_html
    homepage_html = requests.get(url_hp_link, headers)
    if is_log:
        print('//Website package required successfully.')
        if is_verbose:
            print(homepage_html.title)
            print(homepage_html.text)
    soup = BeautifulSoup(homepage_html.content, "lxml")
    tmp_01 = str(soup.table('a'))
    # save all lyric website into a txt file
    foo = open('011_lyric_list_crawler_website_links.txt', 'w+')
    counter_01 = 1
    has_link = tmp_01.find('www')
    while has_link != -1:
        idx_01 = has_link
        idx_02 = tmp_01.find('\"', idx_01)
        link_tmp = str(counter_01) + '\n' + tmp_01[idx_01:idx_02] + '\n'
        foo.writelines(link_tmp)
        if is_verbose+1:
            print(link_tmp)
        # update has_link
        tmp_01 = tmp_01[idx_02:]
        counter_01 += 1
        has_link = tmp_01.find('www')
    foo.close()
    if is_log:
        print('//foo.closed')
        print('//done')




# main()
# try:
#     get_web_list()
# except:
#     print('get_web_list() failed.')
get_web_list()



