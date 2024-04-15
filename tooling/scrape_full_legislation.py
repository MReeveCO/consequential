from bs4 import BeautifulSoup
import requests
import lxml
from time import sleep
import json
import os

years = [2024, 2023]
max_number_of_legislation = 57


# url = f'https://www.legislation.gov.uk/ukpga/2023/55/data.xml'
# response = requests.get(url)
# # soup = BeautifulSoup(response.text, 'xml')
# with open('2023-55.xml', 'w') as f:
#     f.write(response.text)

for year in years:
    for leg in range(max_number_of_legislation):
        url = f'https://www.legislation.gov.uk/ukpga/{year}/{leg+1}/data.xml'

        response = requests.get(url)
        if response.ok:
            document = []
            soup = BeautifulSoup(response.text, 'xml')
            act = soup.title.string

            if not (os.path.isfile(f'../legislation/{act}.json') and os.path.exists(f'../legislation/{act}.json')):
                year = int(soup.title.string[-4:])

                section_ids = [section.P1.get("id")
                               for section in soup.find_all("P1group")]
                section_ids = [
                    section for section in section_ids if section is not None]

                for section in section_ids:
                    if 'section-' in section:
                        print(
                            f'* Processing section {section.replace("section-", "")}')
                        section_number = section.replace('section-', '')
                        section_text = soup.find(id=section).get_text(
                            " ").replace('\n', '')
                        section_title = (
                            soup.find(id=section).parent.find('Title').get_text(" "))
                        sect = {
                            'act': act,
                            'year': year,
                            'section': section_number,
                            'section_title': section_title,
                            'section_text': section_text
                        }
                        document.append(sect)
                print(f'* Writing legislation for {act}')
                with open(f'../legislation/{act}.json', 'w') as f:
                    json.dump(document, f)
            else:
                print(f'== Already outputted {act}')


print('* DONE!')
