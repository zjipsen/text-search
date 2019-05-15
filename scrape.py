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

def format_nav_string(str):
	return unicode(str).encode('ascii','ignore')


url = 'https://zanzaban.tumblr.com'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')
#listelement = soup.find_all('li', attrs={'class':'text-body'})
textposts = soup.find_all('ul', attrs={'class':'post-content', 'class': 'type-text'})


for post in textposts:
	textbody = post.find('li', class_="text-body")
	# caption = post.find('li', attrs={'class':'caption'})
 	text = []
	# p = content.find_all('p')
	if (textbody != None):
		for p in textbody.find_all('p'):
			string = p.string
			if (string != None):
				text.append(format_nav_string(string))

		for a in textbody.find_all('a'):
			print(a.class_)
			string = a.string
			if (string != None):
				text.append(format_nav_string(string))

		for h1 in textbody.find_all('h1'):
			string = h1.string
			if (string != None):
				text.append(format_nav_string(string))

		for h2 in textbody.find_all('h2'):
			string = h2.string
			if (string != None):
				text.append(format_nav_string(string))


	postID = post['id']
	# print(post)
	print('$$$$$')
	# print(text)






















