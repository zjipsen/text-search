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
		text = text + find_text_on_tag(textbody, 'b')
		text = text + find_text_on_tag(textbody, 'i')
		text = text + find_text_on_tag(textbody, 'small')
		text = text + find_text_on_tag(textbody, 'a')
		text = text + find_text_on_tag(textbody, 'h1')
		text = text + find_text_on_tag(textbody, 'h2')
		text = text + find_text_on_img(textbody, 'img')

	tags = post.find('ul', attrs={'class':'tags'})
	if (tags != None):
		text = text + find_text_on_tag(tags, 'a')
		text = text + find_text_on_tag(tags, 'p')

	return text