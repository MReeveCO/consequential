from bs4 import BeautifulSoup
import requests
import lxml
from time import sleep
import json
import os

years = range(1992, 1800, -1)
max_number_of_legislation = 70


def act_splitter(act, year):
    repealed = False
    if 'repealed' in act.lower():
        repealed = True
        brack_start = act.rfind('(')
        unrepealed_act = act[:brack_start].strip()
    else:
        unrepealed_act = act
    try:
        act_year = int(unrepealed_act[-4:])
    except:
        act_year = year

    return (act, act_year, repealed)


for year in years:
    for leg in range(max_number_of_legislation):
        url = f'https://www.legislation.gov.uk/ukpga/{year}/{leg+1}/data.xml'

        response = requests.get(url)
        if response.ok:
            document = []
            soup = BeautifulSoup(response.text, 'xml')
            act = soup.title.string
            (act, act_year, repealed) = act_splitter(act, year)

            if not ((os.path.isfile(f'../legislation/{act_year}/{act}.json') and os.path.exists(f'../legislation/{act_year}/{act}.json')) or (os.path.isfile(f'../repealed/{act_year}/{act}.json') and os.path.exists(f'../repealed/{act_year}/{act}.json'))):
                print(f'* Examining {act}')

                section_ids = []
                for section in soup.find_all("P1group"):
                    if section.P1:
                        section_ids.append(section.P1.get("id"))
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
                            'year': act_year,
                            'section': section_number,
                            'section_title': section_title,
                            'section_text': section_text
                        }
                        document.append(sect)
                print(f'* Writing legislation for {act}')
                if repealed:
                    if not os.path.exists(f'../repealed/{act_year}'):
                        os.mkdir(f'../repealed/{act_year}')
                    with open(f'../repealed/{act_year}/{act}.json', 'w') as f:
                        json.dump(document, f)
                else:
                    if not os.path.exists(f'../legislation/{act_year}'):
                        os.mkdir(f'../legislation/{act_year}')
                    with open(f'../legislation/{act_year}/{act}.json', 'w') as f:
                        json.dump(document, f)
            else:
                print(f'== Already outputted {act}')


print('* DONE!')
