from bs4 import BeautifulSoup
from textblob import TextBlob
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
    
    def polarity(self):
        page_source = requests.get(self.url).text
        soup = BeautifulSoup(page_source, 'html.parser')
        paragraph_list = [element.text for element in soup.find_all('p')]
        content = " ".join(paragraph_list)
        polarity = TextBlob(content).sentiment.polarity
        return polarity
    
    def subjectivity(self):
        page_source = requests.get(self.url).text
        soup = BeautifulSoup(page_source, 'html.parser')
        paragraph_list = [element.text for element in soup.find_all('p')]
        content = " ".join(paragraph_list)
        subjectivity = TextBlob(content).sentiment.subjectivity
        return subjectivity
