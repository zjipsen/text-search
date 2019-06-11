import pickle
import requests
from bs4 import BeautifulSoup

def encode_string(str):
	""" 
	takes in a NavigableString (special type from BeautifulSoup4) and converts to ascii encoded python string
	"""
	return unicode(str).encode('ascii','ignore')


def format_strings(str):
	"""
	takes in a python string and returns array of individual words
	removes punctuation from beginning and end

	TODO: /numerals/most common words (the, a, it)
	TODO: REMOVE PUNCTUATION FROM MIDDLE OF WORD (may split it into 2 words!)
	"""
	words = str.split(' ')
	formatted_words = []
	for word in words:
		formatted_word = word.lower();
		formatted_word = formatted_word.strip('.!?*()&^%$@,;:#\'\"\n')
		if (formatted_word != ''):
			formatted_words.append(formatted_word)
	return formatted_words

def find_text_on_tag(markup, tag):
	"""
	takes in the beautifulSoup object and finds all text contained in all tags of type tag (for example, <p/> or <a/>)
	"""
	text = []

	for elem in markup.find_all(tag):
		string = elem.string
		if (string != None):
			text.extend(format_strings(encode_string(string)))
	return text

def find_text_on_img(markup, tag):
	text = []

	for elem in markup.find_all(tag):
		if (u'alt' in elem.attrs):
			alt_text = elem.attrs[u'alt']
			text.extend(format_strings(encode_string(alt_text)))
		string = elem.string
		if (string != None):
			text.extend(format_strings(encode_string(string)))
	return text

def find_all_text(post):
	textbody = post.find('li')
	# caption = post.find('li', attrs={'class':'caption'})
	text = []

	if (textbody != None):
		text = text + find_text_on_tag(textbody, 'p')
		text = text + find_text_on_tag(textbody, 'a')
		text = text + find_text_on_tag(textbody, 'h1')
		text = text + find_text_on_tag(textbody, 'h2')
		text = text + find_text_on_img(textbody, 'img')

	tags = post.find('ul', attrs={'class':'tags'})
	if (tags != None):
		text = text + find_text_on_tag(tags, 'a')
		text = text + find_text_on_tag(tags, 'p')

	return text

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

def search(words):
	print("searching for the words \"" + str(words) + "\":")
	words = words.split(' ')
	intersect = None
	for word in words:
		if (word in words_to_ids):
			if (intersect == None):
				intersect = words_to_ids[word]
			intersect = words_to_ids[word].intersection(intersect)
	if (intersect == None):
		return None
	return create_links(intersect)

def main():
	global url
	url = 'https://zanzaban.tumblr.com'

	global words_to_ids
	global ids_to_text
	words_to_ids = load_obj('words_to_ids')
	ids_to_text = load_obj('ids_to_text')

	# download_content(100)
	query = 'tiktok'
	search_results = search(query)
	print(search_results if (search_results) else "No results found for the query \"" + str(query) + "\"")
	save_dictionaries()


if __name__ == '__main__':
	main()
# run_tests()















