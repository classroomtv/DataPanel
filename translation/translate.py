'''
Script to translate all the .po files using 
.csv files 
'''

import pandas as pd
import polib
from os.path import join

languages_list = ['en', 'es']
files_list = ['General_Statistics', 'Analysis_by_Institution']

if __name__ == "__main__":
    for lang in languages_list:
        folder_path = f'locales/{lang}/LC_MESSAGES'
        for file_name in files_list:
            translation_sheet = pd.read_csv(f'translation_sheets/{file_name}.csv')
            translation_strings_id = translation_sheet['id'].to_list()

            pofile_path = join(folder_path, file_name + '.po')
            pofile = polib.pofile(pofile_path)

            for entry in pofile:
                if entry.msgid in translation_strings_id:
                    translated_entry = translation_sheet[translation_sheet['id']==entry.msgid]
                    translated_str = translated_entry[lang].to_string(index = False)
                    entry.msgstr = translated_str
                else:
                    print(f'Translation not found for: {entry.msgid}')
            # save new po file
            pofile.save(pofile_path)
            # and compile it
            pofile.save_as_mofile(join(folder_path, file_name + '.mo'))