from bs4 import BeautifulSoup
from ecommercetools import seo
import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide", page_title="Google Search Results of a Keyword")

def get_serp_results(keyword_argument):
	def get_word_count(argument):
	    full_url = argument
	    page_source = requests.get(full_url).text
	    soup = BeautifulSoup(page_source, 'lxml')
	    paragraph_list = [element.text for element in soup.find_all('p')]
	    word_count = len(str(paragraph_list).split())
	    return word_count

	def get_content(argument):
	    full_url = argument
	    page_source = requests.get(full_url).text
	    soup = BeautifulSoup(page_source, 'lxml')
	    paragraph_list = [element.text for element in soup.find_all('p')]
	    content = ''.join(paragraph_list[0:3])
	    return content

	df = seo.get_serps(keyword_argument)
	df.columns = ["Page Title", "URL", "Text"]
	word_count = [get_word_count(element) for element in df["URL"]]
	df["Word Count <p>"] = word_count
	content = [get_content(element) for element in df["URL"]]
	df["Excerpt <p>"] = content
	return df

st.title("*Google Search Results*")

with st.form(key='my_form'):
	keyword = st.text_input(label='Enter keyword here')
	submit_button = st.form_submit_button(label='Get SERP Results')

if submit_button:
	st.header(f"***SERP Results for '{keyword}'***")
	st.table(get_serp_results(keyword))
	st.header("***Related Keywords***")
	st.table(seo.google_autocomplete(keyword, include_expanded=True))
