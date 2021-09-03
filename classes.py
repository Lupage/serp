from bs4 import BeautifulSoup
import requests

class Page:
    def __init__(self, url):
    	self.url = url

    def word_count(self):
    	page_source = requests.get(self.url).text
    	soup = BeautifulSoup(page_source, 'html.parser')
    	paragraph_list = [element.text for element in soup.find_all('p')]
    	word_count = len(str(paragraph_list).split())
    	return word_count

    def content(self):
        page_source = requests.get(self.url).text
        soup = BeautifulSoup(page_source, 'html.parser')
        paragraph_list = [element.text for element in soup.find_all('p')]
        content = " ".join(paragraph_list)
        return content
