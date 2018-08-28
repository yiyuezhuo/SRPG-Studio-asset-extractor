# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 11:33:06 2018

@author: yiyuezhuo
"""

import struct
import os
import string

    
def U(fmt, offset):
    return struct.unpack_from(fmt, data, offset=offset)

def unicode_char2str(unicode_char):
    char_l = []
    for i in range(0,len(unicode_char)-2,2):
        if unicode_char[i+1] == b'\x00':
            char_l.append(unicode_char[i].decode())
        else:
            char_l.append(b''.join(unicode_char[i:i+2]).decode())
    return ''.join(char_l)

pattern = {
        0:[r'Graphics\mapchip','png'],
        1:[r'Graphics\charchip','png'],
        2:[r'Graphics\face','png'],
        3:[r'Graphics\icon','png'],
        4:[r'Graphics\motion','png'],
        5:[r'Graphics\effect','png'],
        6:[r'Graphics\weapon','png'],
        7:[r'Graphics\bow','png'],
        8:[r'Graphics\thumbnail','png'],
        9:[r'Graphics\battleback','jpg'],
        10:[r'Graphics\eventback','jpg'],
        11:[r'Graphics\screenback','png'],
        12:[r'Graphics\worldmap','png'],
        13:[r'Graphics\eventstill','png'],
        14:[r'Graphics\charillust','png'],
        15:[r'Graphics\picture','png'],
        16:[r'Audio\music','ogg'],
        17:[r'Audio\sound','ogg'],
        18:[r'UI\menuwindow','png'],
        19:[r'UI\textwindow','png'],
        20:[r'UI\title','png'],
        21:[r'UI\number','png'],
        22:[r'UI\bignumber','png'],
        23:[r'UI\gauge','png'],
        24:[r'UI\line','png'],
        25:[r'UI\risecursor','png'],
        26:[r'UI\mapcursor','png'],
        27:[r'UI\pagecursor','png'],
        28:[r'UI\selectcursor','png'],
        29:[r'UI\scrollcursor','png'],
        30:[r'UI\panel','png'],
        31:[r'UI\faceframe','png'],
        32:[r'UI\screenframe','png'],
        33:[r'Fonts','.unknowFontFormat'], # since runtime don't have any sample file, I don't know the exact suffix
        34:[r'Video','.unknowVideoFormat'] # since runtime don't have any sample file, I don't know the exact suffix
}



def get_folder_file_offset_list(folder_offset):
    folder_file_num = U('I', folder_offset)[0]
    folder_file_offset_list = []
    for i in range(folder_file_num):
        relative_offset = U('I', folder_offset + 0x4 + i*0x4)[0]
        folder_file_offset_list.append(folder_offset + relative_offset)
    return folder_file_offset_list

    
def get_file_content(file_offset):
    name_len = U('I',file_offset)[0]
    base_name = unicode_char2str(U(str(name_len)+'c',file_offset + 0x4))
    meta = U('3I', file_offset+0x4+name_len*0x1)
    num_file = meta[2]
    
    content_size_list = U(str(num_file)+'I', file_offset+0x4+name_len*0x1 + 3*0x4)
    
    file_list = []
    content_offset = file_offset+0x4+name_len*0x1 + 3*0x4 + num_file*0x4
    for i in range(num_file):
        name = base_name if i==0 else base_name + '-' + string.ascii_letters[i-1]
        
        file_info = dict(
            start_offset = file_offset,
            name = name,
            meta = meta,
            content_size = content_size_list[i],
            content_offset = content_offset
        )
        file_list.append(file_info)
        content_offset += content_size_list[i]
        
    return file_list
    '''
    for idx in num_
        content_size = U('I', file_offset+0x4+name_len*0x1 + 3*0x4)[0]
        content_offset = file_offset+0x4+name_len*0x1 + 3*0x4 + 0x4
        return dict(start_offset = file_offset, name = name, meta = meta, 
                    content_size = content_size, content_offset = content_offset)
    '''

    
def raw_extract(dir_path, verbose = True):
    ''' This way don't require pattern '''
    for i,folder_file_offset_list in enumerate(all_folder_file_offset_list):
        sub_dir_path = os.path.join(dir_path, str(i))
        os.makedirs(sub_dir_path, exist_ok = True)
        for file_offset in folder_file_offset_list:
            for file_info in get_file_content(file_offset):
                name = file_info['name'] if file_info['name'] != '' else 'this_file_dont_have_name_in_rts_file_interesting'
                file_path = os.path.join(sub_dir_path, name)
                with open(file_path, 'wb') as f:
                    f.write(data[file_info['content_offset']:file_info['content_offset']+file_info['content_size']])
                if verbose:
                    print(f'extract -> {file_path}')
                
def extract(dir_path, verbose=True):
    ''' This way require pattern but more informative '''
    for i,folder_file_offset_list in enumerate(all_folder_file_offset_list):
        sub_dir_path = os.path.join(dir_path, pattern[i][0])
        os.makedirs(sub_dir_path, exist_ok = True)
        for file_offset in folder_file_offset_list:
            for file_info in get_file_content(file_offset):
                name = file_info['name'] if file_info['name'] != '' else 'this_file_dont_have_name_in_rts_file_interesting'
                file_path = os.path.join(sub_dir_path, name+'.'+pattern[i][1])
                with open(file_path, 'wb') as f:
                    f.write(data[file_info['content_offset']:file_info['content_offset']+file_info['content_size']])
                if verbose:
                    print(f'extract -> {file_path}')
                

def setup(asset_path = 'runtime.rts'):
    global data, head, total_size
    global folder_offset_list, all_folder_file_offset_list, all_folder_file_info_list
    
    with open(asset_path, 'rb') as f:
        data = f.read()
    
    head = U('8c', 0x0)
    total_size = U('I', 0x8)[0]
    
    first_folder_offset = U('I', 0xc)[0]
    
    folder_offset_list = []
    offset = 0xc
    while offset < first_folder_offset:
        folder_offset_list.append(U('I', offset)[0])
        offset += 0x4
    
    
    all_folder_file_offset_list = []
    for i in range(len(folder_offset_list)):
        folder_offset = folder_offset_list[i]
        next_folder_offset = folder_offset_list[i+1] if i+1<len(folder_offset_list) else total_size
        if next_folder_offset - folder_offset > 0:
            folder_file_offset_list = get_folder_file_offset_list(folder_offset)
            all_folder_file_offset_list.append(folder_file_offset_list)
        else:
            all_folder_file_offset_list.append([])
    
    
    all_folder_file_info_list = []
    for folder_file_offset_list in all_folder_file_offset_list:
        folder_file_info_list = []
        for file_offset in folder_file_offset_list:
            folder_file_info_list.append(get_file_content(file_offset))
        all_folder_file_info_list.append(folder_file_info_list)

if __name__ == '__main__':
    setup('runtime.rts')
    #extract('output')

'''
# TEST
first_folder_file_num = U('I', first_folder_offset)[0]
first_folder_file_offset_list = []
for i in range(first_folder_file_num):
    relative_offset = U('I', first_folder_offset + 0x4 + i*0x4)[0]
    first_folder_file_offset_list.append(first_folder_offset + relative_offset)
    
first_file_offset = first_folder_file_offset_list[1]
first_name_len = U('I',first_file_offset)[0]
first_name = unicode_char2str(U(str(first_name_len)+'c',first_file_offset + 0x4))
first_meta = U('3I', first_file_offset+0x4+first_name_len*0x1)
first_content_size = U('I', first_file_offset+0x4+first_name_len*0x1 + 3*0x4)[0]
first_content_offset = first_file_offset+0x4+first_name_len*0x1 + 3*0x4 + 0x4
'''
