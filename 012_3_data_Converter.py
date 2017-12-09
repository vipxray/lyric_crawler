# Author: Haorui Chen
# Update: Dec 7, 2017

import ast

# switch
is_verbose = 0
is_log = 1


# variables
tmp_file_lyric_data = []
# tmp_lyric_data = []
cur_file_name = ''
op_file_name = ''

# how many lyric read in one file
lrNO = 100
# how many file to read
frNO = 5

count_1 = 0


def readF(fileName):
    try:
        tmp_file_lyric_list = []
        foo_1 = open(fileName, 'r+')
        first_line = foo_1.readline()
        if is_log:
            print('Reading file: ' + fileName)
            start_letter = first_line[13:14]
            page_idx = first_line[28:29]
            print('\t- file idx: lyric stating letter: ' + start_letter +
                  '; page_idx in search result: ' + str(page_idx))
    except:
        print('>>> ERROR: method readF(fName): Failed to open the data file. ##X##')
    
    try:
        # for each lyric, return a list contains: title, author, lyric
        idx_lyric = 0
        nextLine = foo_1.readline()
        # while nextLine:
        for idx_lyric in range(0, lrNO):
            if is_verbose:
                print('- lyric NO.: ' + str(idx_lyric))
            append_rtn_list = readLyric(nextLine)
            if append_rtn_list == -1:
                break
            tmp_file_lyric_list.append(append_rtn_list)
            # tmp_file_lyric_list.append(readLyric(nextLine))
            nextLine = foo_1.readline()
        # return data
        if is_log:
            print('\t- Total ' + str(len(tmp_file_lyric_list)) + ' lyrics returned.')
        # return the lyric list in json format
        foo_1.close()
        return tmp_file_lyric_list
    except:
        print('>>> ERROR: method readF(fName): return lyric data failed. ##X##')

def readLyric(currentLn):
    rtn_data = []
    # get info from string and save into list
    if currentLn == "":
        return -1
    try:
        currentLn = currentLn[2:len(currentLn) - 3]
        currentLn = currentLn.replace('Lyrics\', \"', 'Lyrics\', \'')
        currentLn = currentLn.replace('Lyrics\", \'', 'Lyrics\', \'')
        currentLn = currentLn.replace('Lyrics\", \"', 'Lyrics\', \'')
        c_parts = currentLn.split('Lyrics\', \'')
        # cut the string into list
        if is_verbose:
            print('\t- ' + c_parts[0])
            print('\t- ' + c_parts[1])
            print('\t- ' + c_parts[2])
        # find the data
        cur_author = c_parts[0]
        cur_title = c_parts[1]
        cur_lyric = str(c_parts[2])
        cur_lyric = cur_lyric.replace('\"', '\\\\\'')
        cur_lyric = cur_lyric.replace('\'', '\\\\\'')
        cur_lyric = cur_lyric.replace('\\t', '\\\\t')
        cur_lyric = cur_lyric.replace('\\n', '\\\\n')
        cur_lyric = cur_lyric.replace('\\r', '\\\\r')
        # get the data
        rtn_data.append(cur_title)
        rtn_data.append(cur_author)
        rtn_data.append(cur_lyric)
        if is_log:
            # print('===========> Reading data: ' + cur_title)
            if is_verbose:
                print('########## author: ' + cur_author)
                print('########## title: ' + cur_title)
                print('--------------------------------------------------------------------------------------')
                print('########## lyric: ' + cur_lyric)
                print('--------------------------------------------------------------------------------------')
        # formate the data into the json file
        ready_to_write = toJson(rtn_data)
        return ready_to_write
    except:
        print('>>> XXX###XXX ERROR: method readLyric(currentLn): return lyric data failed. ##X##')
        print('>>>' + currentLn)

def toJson(lyric_data_set):
    # {   "title": {
    #         "title": "",
    #         "author": "",
    #         "lyric": ""
    #     }
    # }
    #
    if is_verbose:
        print(lyric_data_set[0])
    j_string = '\"' + str(lyric_data_set[0]) + '\": {' + '\"title\":\"' + str(lyric_data_set[0]) + '\",' \
               + '\"author\":\"' + lyric_data_set[1] + '\",\"lyric\":\"' + lyric_data_set[2] + '\"}'
    if is_verbose:
        print('toJson(lyric_data_set): ' + j_string)
    return j_string

def write_into_file(cur_lyric_list, jsonFN):
    jsonFN = jsonFN + '.json'
    foo_2 = open(jsonFN, 'w+')
    foo_2.write('{')
    idx_cll = 0
    try:
        cll_len = len(cur_lyric_list)
    except:
        print('Exception: cur_lyric_list: ' + cur_lyric_list)
        return -1
    for idx_cll in (0, len(cur_lyric_list)-2):
        tmpx1 = str(cur_lyric_list[idx_cll])
        foo_2.write(tmpx1)
        foo_2.write(',')
    foo_2.write(cur_lyric_list[len(cur_lyric_list)-1])
    foo_2.write('}')
    foo_2.close()
    if is_log:
        if is_verbose:
            print('Done writing: ' + jsonFN)









##############
### MAIN() ###

# for each file, read each lyric in the file

for fN_num in range(0, frNO):
    fName = str('09') + str(fN_num) + '_lyric_data_package.txt'
    # read file and return lyrics for current file
    # in each file, read all lyric and return json string
    cur_lyric_data_list = readF(fName)

    # store current data into a json file
    fName2 = fName[:len(fName)-5]
    # write the file
    write_into_file(cur_lyric_data_list, fName2)
    print('JSON file: ' + fName2 + ' written.')

    # if write_into_file(cur_lyric_data_list, fName2) == -1:
    #     print('JSON file: ' + fName2 + ' written.')
    #     print('XXXXXXXXXXX')
    #     print(cur_lyric_data_list)

    if is_log:
        print('=====================================================================')
        # print('check returned data:')
        # for cld in cur_lyric_data_list:
        #     print(cld)
        #     print(' Obtained.')
    # print('>>> ERROR: readF(fName) failed. ##X##')