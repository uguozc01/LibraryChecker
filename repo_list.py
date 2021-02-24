from bs4 import BeautifulSoup
import requests
import re

class Repos:
    base_url = 'https://github.com'

    def __init__(self, user, language):

        self.user = user
        self.language = language
        self.href_list = []

    def repo_links(self):

        user_repo = f'{self.base_url}/{self.user}?tab=repositories'
        source = requests.get(user_repo)
        soup = BeautifulSoup(source.text, 'lxml')
        user_repos = soup.find_all('h3', {'class':'wb-break-all'})

        repo_list = [f"{self.base_url}{repo.a['href']}" for repo in user_repos]

        for i in range(len(repo_list)):
            repo_source_i = requests.get(repo_list[i])
            soup_repo_i = BeautifulSoup(repo_source_i.text, 'lxml')
            anchor_i = soup_repo_i.find_all('a', {'href' : re.compile('\.' + self.language)})
            for item in anchor_i:
                ref = item['href']
                self.href_list.append(f'{self.base_url}/{ref}')
        return self.href_list