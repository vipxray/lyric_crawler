# Author: Haorui Chen
# Update: Nov 6, 2017

import ast

# switch
is_verbose = 0
is_log = 1


# variables
tmp_file_lyric_data = []
# tmp_lyric_data = []




def readF(fileName):
    print('Reading file: ' + fileName)
    tmp_file_lyric_list = []
    foo_1 = open(fileName, 'r+')
    print(foo_1.readline())
    tmp_line_list = []
    # for each lyric, return a list contains: title, author, lyric
    for idx_lyric in (0, 3):
        try:
            tmp_line = foo_1.readline()
            x = ast.literal_eval(tmp_line)
            # find the data
            cur_author = x[0]
            cur_author = cur_author[0:cur_author.find(' Lyric')]
            cur_title = x[1]
            cur_title = cur_title[0:cur_title.find(' Lyric')]
            cur_lyric = x[2]
            rtn_data = []
            rtn_data.append(cur_title)
            rtn_data.append(cur_author)
            rtn_data.append(cur_lyric)
            tmp_file_lyric_list.append(rtn_data)
            if is_log:
                if is_verbose:
                    print('=============================================')
                    print('>>> is_log: ' + cur_title + 'lyric info obtained.')
                    print('Author: ' + cur_author)
                    print('---------------------------------------------')
                    print('Lyric: ')
                    print(cur_lyric)
                    print('=============================================')
        except:
            print('>>> ERROR: method readF(fName): obtaining lyric failed. ##X##')
    try:
        # return data
        return tmp_file_lyric_list
    except:
        print('>>> ERROR: method readF(fName): return lyric data failed. ##X##')

def readFile(fileName):
    print('Reading file.')


##############
### MAIN() ###


for fN_num in range(0, 2):
    fName = str('09') + str(fN_num) + '_lyric_data_package.txt'

    cur_lyric_data = readF(fName)
    if is_log:
        for cld in cur_lyric_data:
            print(cld[0])
            print(' Obtained.')

    # print('>>> ERROR: readF(fName) failed. ##X##')