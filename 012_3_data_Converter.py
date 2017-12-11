# Author: Haorui Chen
# Update: Dec 10, 2017


# switch #
is_verbose = 0
is_log = 1

# variables #
tmp_file_lyric_data = []
# tmp_lyric_data = []
cur_file_name = ''
op_file_name = ''
# how many lyric read in one file
lrNO = 100
# how many file to read
frNO = 1


# Methods:
def readF(fileName):
    # open file
    try:
        tmp_file_lyric_list = []
        foo_1 = open(fileName, 'r+')
        # read first line of file information
        first_line = foo_1.readline()
        if is_log:
            start_letter = first_line[13:14]
            page_idx = first_line[28:29]
            print('Reading file: ' + fileName + ',\t|\tlyric stating letter:__'
                  + start_letter + '__\t|\tpage_idx in search result:__' + str(page_idx) + '__')
    except:
        print('>>> ERROR: method readF(fName): Failed to open the data file. ##X##')
    # read each line in current file, then use readLyric() to reformat and return the json format lyrics data
    try:
        idx_lyric = 0
        nextLine = foo_1.readline()
        while nextLine:
            if is_verbose:
                print('\t    verbose - lyric NO.: ' + str(idx_lyric))
            # read the current line lyric and return the json format lyric data.
            append_rtn_list = readLyric(nextLine)
            # if failed to read the lyric
            if append_rtn_list == -1:
                break
            # append each line data into the tmp_file_lyric_list waiting for return
            tmp_file_lyric_list.append(append_rtn_list)
            nextLine = foo_1.readline()
        if is_verbose:
            print('\t- Total ' + str(len(tmp_file_lyric_list)) + ' lyrics returned.')
        # return the lyric list in json format
        foo_1.close()
        return tmp_file_lyric_list
    except:
        print('>>> ERROR: method readF(fName): return lyric data failed. ##X##')

def readLyric(currentLn):
    rtn_data = []
    # get info from string and save into list
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
        cur_lyric = cur_lyric.replace('\'', '\\\\\'')
        cur_lyric = cur_lyric.replace('\\\\\\\'', '\\\\\'')
        cur_lyric = cur_lyric.replace('\"', '\\\\\'')
        cur_lyric = cur_lyric.replace('\\t', '\\\\t')
        cur_lyric = cur_lyric.replace('\\n', '\\\\n')
        cur_lyric = cur_lyric.replace('\\r', '\\\\r')
        # append the data to rtn_data[]
        rtn_data.append(cur_title)
        rtn_data.append(cur_author)
        rtn_data.append(cur_lyric)
        if is_verbose:
            print('\t verbose - author: ' + cur_author + '\n\t verbose - title: ' + cur_title)
            print('\t verbose - orgional lyric: ' + str(c_parts[2])[0:50])
            print('\t verbose - new lyric     : ' + cur_lyric[0:50])
            print('\t-----------------------------------------------------------------------------')
    except:
        print('\t  ERROR: method readLyric(currentLn): Reading current lyric failed!')
        print('\t  >>> currentLn: ' + currentLn)
        return -1
    # translate the rtn_data into the json format
    ready_to_write = toJson(rtn_data)
    return ready_to_write

def toJson(lyric_data_set):
    # Json format
    # {   "current_title1": {    "title":"current_title1", "author":"current_author1", "lyric":"current_lyric1"},
    #     "current_title2": {    "title":"current_title2", "author":"current_author2", "lyric":"current_lyric2"},
    #     ......
    # }
    try:
        j_string = '\"' + str(lyric_data_set[0]) + '\": {' + '\"title\":\"' + str(lyric_data_set[0]) + '\",' \
               + '\"author\":\"' + lyric_data_set[1] + '\",\"lyric\":\"' + lyric_data_set[2] + '\"}'
        if is_verbose:
            print('\t    verbose - author: ' + lyric_data_set[0] + '\n\t    verbose - title: ' + lyric_data_set[1])
            print('\t    verbose - orgional lyric: ' + str(lyric_data_set[2])[0:50])
            print('\t    verbose - j-format: ' + j_string[0:55])
            print('\t    ---------------------------------------------------------------------------')
    except:
        print('\t  ERROR: method toJson(lyric_data_set): reformat current lyric failed!')
        print('\t  lyric_data_set: title: ' + lyric_data_set[0])
        print('\t           author:       ' + lyric_data_set[1])
        print('\t            lyric:       ' + lyric_data_set[2][0:52])
        print('\t-----------------------------------------------------------------------------')
    return j_string

def write_into_file(cur_lyric_list, jsonFN):
    try:
        count_1 = 0
        jsonFN = jsonFN + '.json'
        foo_2 = open(jsonFN, 'w+')
        foo_2.writelines('{')
        idx_cll = 0
        try:
            cll_len = len(cur_lyric_list)
        except:
            print('\t  ERROR: method write_into_file(cur_lyric_list, jsonFN): Reading current lyric failed!')
            print('\t  cur_lyric_list length: ' + cll_len)
            print('\t-----------------------------------------------------------------------------')
            print('Exception: cur_lyric_list: ' + cur_lyric_list)
        # write all lyric into the json file
        for idx_cll in range(0, cll_len-1):
            tmpx1 = str(cur_lyric_list[idx_cll])
            foo_2.write(tmpx1)
            count_1 += 1
            foo_2.write(',')
        foo_2.writelines(cur_lyric_list[len(cur_lyric_list)-1])
        foo_2.writelines('}')
        foo_2.close()
        if is_log:
            if is_verbose:
                print('\t    verbose - cur_lyric_list len(): ' + str(len(cur_lyric_list)))
                print('\t    verbose - writing lyric number check: ' + str(count_1+1))
                print('\t    verbose - Done writing: ' + jsonFN)
    except:
        print('\t  ERROR: method write_into_file(cur_lyric_list, jsonFN): storing lyric failed! File: ' + jsonFN)



###############################################
# MAIN() #

# for each file, read each lyric in the file
for fN_num in range(0, frNO):
    # assemble file name
    fName = str('09') + str(fN_num) + '_lyric_data_package.txt'
    # read file and return lyrics for current file
    #   in each file, read all lyric and return json string
    cur_lyric_data_list = readF(fName)
    if is_verbose:
        print('\t    verbose - checking cur_lyric_data_list[] in json format.')
        chk_cldl_idx = 0
        for cldl in cur_lyric_data_list:
            print('\t    cldl[' + str(chk_cldl_idx) + '] | ' + str(cldl)[0:150])
            chk_cldl_idx += 1
    # store current file's data into a json file
    fName2 = fName[:len(fName)-5]
    # write the file
    write_into_file(cur_lyric_data_list, fName2)
    print('JSON file:    ' + fName2 + ' written.')
    if is_log:
        print('=====================================================================')
