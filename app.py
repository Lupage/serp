from classes import Page
from ecommercetools import seo
from difflib import SequenceMatcher
import pandas as pd
import re
import requests
import streamlit as st

st.set_page_config(layout="wide", page_title="Google Search Results of a Keyword")

def get_serp_results(keyword_argument):
	df = seo.get_serps(keyword_argument)
	df.columns = ["Page Title", "URL", "Description From SERP"]
	word_count = [Page(element).word_count() for element in df["URL"]]
	df["Word Count <p>"] = word_count
	keyword_in_title = [keyword_argument.lower() in element.lower() for element in df["Page Title"]]
	df["Is Keyword in Page Title?"] = keyword_in_title
	matcher = [SequenceMatcher(None, keyword_argument.lower(), element.lower()).ratio()*100 for element in df["Page Title"]]
	matcher = [str("{:.2f}".format(element))+"%" for element in matcher]
	df["How Identical is Page Title to Keyword?"] = matcher
	sentiment = [Page(element).polarity() for element in df["URL"]]
	df["Sentiment"] = sentiment
	subjectivity = [Page(element).subjectivity() for element in df["URL"]]
	df["Subjectivity"] = subjectivity
	return df

st.title("*Google Search Results*")

with st.form(key='my_form'):
	keyword = st.text_input(label='Enter keyword here')
	submit_button = st.form_submit_button(label='Get SERP Results')
	
if submit_button:
	df = get_serp_results(keyword)
	st.header(f"***SERP Results for '{keyword}'***")
	st.table(df[["Page Title", "URL", "Word Count <p>", "Is Keyword in Page Title?", "How Identical is Page Title to Keyword?", "Sentiment", "Subjectivity"]])
	st.header("***Related Keywords***")
	autocomplete_df = seo.google_autocomplete(keyword, include_expanded=True)
	st.table(autocomplete_df)
