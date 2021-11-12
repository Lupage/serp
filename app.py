from bs4 import BeautifulSoup
from ecommercetools import seo
import streamlit as st
import pandas as pd
import requests
from difflib import SequenceMatcher

st.set_page_config(layout="wide", page_title="Google Search Results of a Keywords")

def get_word_count(url_argument):
	full_url = url_argument
	page_source = requests.get(full_url).text
	soup = BeautifulSoup(page_source, 'html.parser')
	paragraph_list = [element.text for element in soup.find_all('p')]
	word_count = len(str(paragraph_list).split())
	return word_count

def get_serp_results(keyword_argument):
	df = seo.get_serps(keyword_argument)
	df.columns = ["Position","Page Title", "URL", "Description From SERP"]
	word_count = [get_word_count(element) for element in df["URL"]]
	df["Word Count <p>"] = word_count
	keyword_in_title = [keyword_argument.lower() in element.lower() for element in df["Page Title"]]
	df["Is Keyword in Page Title?"] = keyword_in_title
	matcher = [SequenceMatcher(None, keyword_argument.lower(), element.lower()).ratio()*100 for element in df["Page Title"]]
	matcher = [str("{:.2f}".format(element))+"%" for element in matcher]
	df["How Identical is Page Title to Keyword?"] = matcher
	return df

st.title("*Google Search Results*")

with st.form(key='my_form'):
	keyword = st.text_input(label='Enter keyword here')
	submit_button = st.form_submit_button(label='Get SERP Results')

if submit_button:
	df = get_serp_results(keyword)
	st.header(f"***SERP Results for '{keyword}'***")
	serp_results = df[["Position", "Page Title", "URL", "Word Count <p>", "Is Keyword in Page Title?", "How Identical is Page Title to Keyword?"]]
	st.table(serp_results)
	st.header("***Related Keywords***")
	keyword_df = seo.google_autocomplete(keyword, include_expanded=True)
	st.table(keyword_df)
