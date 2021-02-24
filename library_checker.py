from repo_list import Repos
from bs4 import BeautifulSoup
import requests
import re

def main():

    user = input('Please enter your github username:\n')
    language = str(input('Please enter programming language extension, e.g. "py" :\n'))
    repo1 = Repos(user,language)
    result = repo1.repo_links()
    pattern1 = re.compile(r'(import)\s(\w+)')
    pattern2 = re.compile(r'(from)\s(\w+)\s(import)\s(\w+)')
    library = []

    for item in result:
        code_page = requests.get(item)
        soup = BeautifulSoup(code_page.text, 'lxml')
        tds = soup.find_all('td', {'class':'blob-code blob-code-inner js-file-line'})
        for td in tds:
            if re.match(pattern1, td.text):
                m1 = re.match(pattern1, td.text)
                if m1.group(2) not in library:
                    library.append(m1.group(2))
            elif re.match(pattern2, td.text):
                m2 = re.match(pattern2, td.text)
                if m2.group(2) not in library and not any( re.search( m2.group(2), item) for item in result ):
                    library.append(m2.group(2))
            elif re.search('from', td.text) and re.search('import', td.text):
                if re.split(r'[.\s]', td.text)[1] not in library:
                    library.append(re.split(r'[.\s]', td.text)[1] )
    print(library)

main()
