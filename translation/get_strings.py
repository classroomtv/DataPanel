'''
Script to get all the msgids (ids from .po file)
from all the pages contained in the platform
'''


import pandas as pd
import polib
from os.path import join

files_list = ['General_Statistics', 'Analysis_by_Institution']

if __name__ == "__main__":
    folder_path = f'locales/en/LC_MESSAGES'
    for file_name in files_list:
        string_list = []
        pofile_path = join(folder_path, file_name + '.po')
        pofile = polib.pofile(pofile_path)

        for entry in pofile:
            string_list.append(entry.msgid)
        strings_df = pd.DataFrame(string_list)
        # save new csv file
        strings_df.to_excel(f'{file_name}_strings.xlsx')