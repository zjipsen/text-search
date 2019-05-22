import requests
import pickle
from bs4 import BeautifulSoup
import formatters

"""
interface description: (find a better IDE because this'll get outdated REALquick)

void save_obj(obj, name)
object load_obj(name)
void run_tests()
void test_format_strings(test_input, expected_output)
void test_find_all_text(test_markup, expected_output)
str encode_string(str)
str[] format_strings(str)
str[] find_text_on_tag(markup, tag)
str[] find_text_on_img(markup, tag)
str[] find_all_text(post)
void store(postID, words) // side effect: stores into global variable
str create_links(ids)
str[] search(word)
void parse_html(html) // calls store
void download_one_page(url)
void download_content(num_pages, start_page=2)
void clear_dictionaries()
"""

"""

VIDEO POST:
<ul class="post-content type-photo OR content-based">
	<li class="content">
		<ul class="post">
	<li class="caption">
		<p> 
			<a> most recent commenter's link; class="tumblr_blog"
		<blockquote> all nested content; contained in chains of <p>, <a>, <h2>, <blockquote>
		<p> optional; most recent comment
		<p>
			<a> via; class="tumblr_blog"
	<ul class="tags"> // optional
	<li class="post_info">


TEXT POST (or photo/video within a text post):
<ul class="post-content type-text">
	<li class="content">
		<ul class="post">
			<li class="text-body"> // includes comments from reblogs
				<p> 
					<a> most recent commenter's link; class="tumblr_blog"
				<blockquote> all nested content; contained in chains of <p>, <a>, <h2>, <blockquote>
				<p> optional; most recent comment
				<p>
					<a> via; class="tumblr_blog"
	<ul class="tags"> // optional
	<li class="post_info">
"""

def save_obj(obj, name):
	with open('obj/'+ name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
	with open('obj/' + name + '.pkl', 'rb') as f:
		return pickle.load(f)

def clear_dictionaries():
	words_to_ids = {}
	ids_to_text = {}
	save_obj(words_to_ids, 'words_to_ids')
	save_obj(ids_to_text, 'ids_to_text')

def store(postID, words):
	"""
	dictionary:
	keyword : set([postID1, postID2...])

	second dictionary?:
	postID : [ 'full', 'text' ]
	"""
	ids_to_text[postID] = words
	for word in words:
		if (word not in words_to_ids):
			words_to_ids[word] = set([postID])
		else:
			words_to_ids[word].add(postID)

def create_links(ids):
	links = ""
	for postID in ids:
		links = links + url + "/" + postID + "\n"
	return links

def search(word):
	print("searching for the word \"" + str(word) + "\":")
	if (word not in words_to_ids):
		return None
	else:
		return create_links(words_to_ids[word])

def main():
	global url
	url = 'https://zanzaban.tumblr.com'

	global words_to_ids
	global ids_to_text
	words_to_ids = load_obj('words_to_ids')
	ids_to_text = load_obj('ids_to_text')

	clear_dictionaries()
	download_content(1)
	query = 'test'
	search_results = search(query)
	print(search_results if search_results != None else "No results found for the query " + str(query))
	save_obj(words_to_ids, 'words_to_ids')
	save_obj(ids_to_text, 'ids_to_text')


if __name__ == '__main__':
	main()
# run_tests()















