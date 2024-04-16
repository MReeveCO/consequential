import os
import json

folders = os.listdir('../legislation')

print(folders)
for f in folders:
    folder_loc = f'../legislation/{f}'
    for file in os.listdir(folder_loc):
        file_content = open(f'{folder_loc}/{file}', 'r')
        file_content = file_content.readlines()[0]
        file_content = json.loads(file_content)
        for section in file_content:
            file_name = f'{section["year"]}-{section["act"]}-{section["section"]}'
            output = open(f'../processed/{file_name}', 'a+')
            output.write(section['act'])
            output.write('\n')
            output.write(f'SECTION {section["section"]}')
            output.write('\n')
            output.write(section['section_title'])
            output.write('\n')
            output.write(section['section_text'])
