import requests
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


def encode_string(str):
	""" 
	takes in a NavigableString (special type from BeautifulSoup4) and converts to ascii encoded python string
	"""
	return unicode(str).encode('ascii','ignore')


def format_strings(str):
	"""
	takes in a python string and returns array of individual words

	TODO: remove punctuation/numerals/most common words (the, a, it)/capitalization/special chars like \n\n to ensure standardized searching
	"""
	return [encode_string(str)]


def find_all_text(markup, tag):
	"""
	takes in the beautifulSoup object and finds all text contained in all tags of type tag (for example, <p/> or <a/>)
	"""
	text = []

	for elem in markup.find_all(tag):
		string = elem.string
		if (string != None):
			text.extend(format_strings(string))
	return text

def find_text_on_img(markup, tag):
	text = []

	for elem in markup.find_all(tag):
		if (u'alt' in elem.attrs):
			alt_text = elem.attrs[u'alt']
			text.extend(format_strings(alt_text))
		string = elem.string
		if (string != None):
			text.extend(format_strings(string))
	return text

def main():
	url = 'https://zanzaban.tumblr.com'
	response = requests.get(url)
	html = response.content

	soup = BeautifulSoup(html, 'html.parser')
	#listelement = soup.find_all('li', attrs={'class':'text-body'})
	textposts = soup.find_all('ul', attrs={'class':'post-content'})

	for post in textposts:
		textbody = post.find('li')
		# caption = post.find('li', attrs={'class':'caption'})
		text = []
		# p = content.find_all('p')
		if (textbody != None):
			text = text + find_all_text(textbody, 'p')
			text = text + find_all_text(textbody, 'a')
			text = text + find_all_text(textbody, 'h1')
			text = text + find_all_text(textbody, 'h2')
			text = text + find_text_on_img(textbody, 'img')

		postID = post['id']
		# print(post)
		print('$$$$$')
		print(text)


main()


















