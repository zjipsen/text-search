import pickle
import requests
from bs4 import BeautifulSoup
from formatters import *

def parse_html(html):
	soup = BeautifulSoup(html, 'html.parser')
	#listelement = soup.find_all('li', attrs={'class':'text-body'})
	textposts = soup.find_all('ul', attrs={'class':'post-content'})
	
	for post in textposts:
		postID = encode_string(post['id'])
		if (postID not in ids_to_text):
			text = find_all_text(post)
			store(postID, text)

def download_one_page(url):
	response = requests.get(url)
	html = response.content
	parse_html(html)

def download_content(num_pages, start_page=2):
	print("downloading page 1...")
	download_one_page(url)
	i = 0
	while (i < num_pages):
		print("downloading page " + str(start_page + i) + "...")
		download_one_page(url + '/page/' + str(start_page + i))
		i += 1

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
	with open('./obj/'+ name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
	with open('./obj/' + name + '.pkl', 'rb') as f:
		return pickle.load(f)

def clear_dictionaries():
	words_to_ids = {}
	ids_to_text = {}
	save_obj(words_to_ids, 'words_to_ids')
	save_obj(ids_to_text, 'ids_to_text')

def save_dictionaries():
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

def search_intersection(words):
	print("searching for posts including the words \"" + str(words) + "\":")
	words = words.split(' ')
	intersect = None
	for word in words:
		if (word in words_to_ids):
			if (intersect == None):
				intersect = words_to_ids[word]
			intersect = words_to_ids[word].intersection(intersect)
		else:
			return None

	if (intersect == None):
		return None
	return create_links(intersect)

def search_union(words):
	print("searching for posts including one or more of the words \"" + str(words) + "\":")
	words = words.split(' ')
	union = set([])
	for word in words:
		if (word in words_to_ids):
			union = union.union(words_to_ids[word])
	if (len(union) == 0):
		return None
	return create_links(union)

def main():
	global url
	url = 'https://johnlacena.tumblr.com'

	global words_to_ids
	global ids_to_text
	words_to_ids = load_obj('words_to_ids')
	ids_to_text = load_obj('ids_to_text')
	# clear_dictionaries()

	download_content(10)
	query = 'phenomenon'
	search_results = search_union(query)
	print(search_results if (search_results) else "No results found for the query \"" + str(query) + "\"")
	save_dictionaries()
	print(words_to_ids)


if __name__ == '__main__':
	main()
# run_tests()















