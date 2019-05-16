import requests
import pickle
from bs4 import BeautifulSoup

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


def run_tests():
	test_format_strings("this is a test",['this','is','a','test'])
	test_format_strings("This Is ANOTHER TEST",['this','is','another','test'])
	test_format_strings("This. ,Is, .ANOTHER. TEST.",['this','is','another','test'])
	test_format_strings("\n\nThis is a test again\n\n.", ['this','is','a','test', 'again'])

	markup1 = '<ul class="post-content type-text     " id="184924945881" style="position: absolute; left: 276px; top: 220px;"><li class="content relative"><ul class="post"><li class="text-body lh-copy"><p>this is a test</p></li></ul></li>'
	expected_words = ['this','is','a','test']
	test_find_all_text(markup1, expected_words)

	markup2 = '<ul class="post-content type-text      is-reblogged" id="184924955921" style="position: absolute; left: 0px; top: 0px;"><li class="content relative"><ul class="post"><li class="text-body lh-copy"><p><a href="https://zanzaban.tumblr.com/post/184924951631/this-is-a-second-test" class="tumblr_blog">zanzaban</a>:</p><blockquote><p>this is a second test</p></blockquote><p>this is a reblog of a test</p></li></ul></li><ul class="tags"><li><a href="https://zanzaban.tumblr.com/tagged/more-different-tags">#more different tags</a></li></ul>'
	expected_words = ['this','is','a','second','test','this','is','a','reblog','of','a','test','zanzaban','more','different','tags']
	test_find_all_text(markup2, expected_words)

	markup3 = '<ul class="post-content type-text     " id="184924948546" style="position: absolute; left: 552px; top: 0px;"><li class="content relative"><ul class="post"><li class="text-title "><h3 class="post-title"><a href="https://zanzaban.tumblr.com/post/184924948546/this-is-a-title">this is a title</a></h3></li><li class="text-body lh-copy"><p>of a test</p></li></ul></li>'
	expected_words = ['of','a','test','this','is','a','title']
	test_find_all_text(markup3, expected_words)

def test_format_strings(test_input, expected_output):
	result = format_strings(test_input)
	if (result != expected_output):
		print("FAIL: Test of format_strings method failed; expected " + str(expected_output) + " but got " + str(result) + " \n\n")
	else:
		print("Test passed")

def test_find_all_text(test_markup, expected_output):
	soup = BeautifulSoup(test_markup, 'html.parser')
	post = soup.find('ul', attrs={'class':'post-content'})

	result = find_all_text(post)
	if (result != expected_output):
		print("FAIL: Test of find_all_text method failed; expected " + str(expected_output) + " but got " + str(result) + " \n\n")
	else:
		print("Test passed")


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
		formatted_word = formatted_word.strip('.!?,;:#\'\"\n')
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

def store(postID, words):
	"""
	dictionary:
	keyword : [postID1, postID2...]

	second dictionary?:
	postID : [ 'full', 'text' ]
	"""
	ids_to_text[postID] = words
	for word in words:
		if (word not in words_to_ids):
			words_to_ids[word] = [postID]
		else:
			words_to_ids[word].append(postID)

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
		return words_to_ids[word]

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

def main():
	global url
	url = 'https://zanzaban.tumblr.com'

	global words_to_ids
	global ids_to_text
	words_to_ids = load_obj('words_to_ids')
	ids_to_text = load_obj('ids_to_text')

	# download_content(25, 99)
	print(create_links(search('cat')))
	save_obj(words_to_ids, 'words_to_ids')
	save_obj(ids_to_text, 'ids_to_text')

main()
# run_tests()















