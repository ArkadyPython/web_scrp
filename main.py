import requests
import bs4
import json
import re
import fake_headers

headers = fake_headers.Headers(browser='firefox', os='win')
headers_dict = headers.generate()
response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers_dict)
html_data = response.text
soup = bs4.BeautifulSoup(html_data, 'lxml')

result = []
for info in soup.find_all(class_ ='vacancy-serp-item__layout'):
    title0 = info.find(class_ = "serp-item__title")
    title = title0.text
    description = info.find(class_ ='g-user-content')
    if description is not None:
        desc = description.text
    else:
        desc = ''
    if 'django' in (desc + title).lower() or 'flask' in (desc + title).lower():
        salary = info.find('span', class_ ='bloko-header-section-2')
        if salary is None:
            salary = ''
        else:
            salary = salary.text
        city = info.find('div', attrs = {'data-qa': 'vacancy-serp__vacancy-address'}).text
        company = info.find('div', class_ ='vacancy-serp-item__meta-info-company').text

        result.append(
            {
                "link": title0.attrs["href"],
                "salary": salary,
                "company": company,
                "city": re.sub('\sи\s.+', '', city)
            }
        )
with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False, indent=2)
