usage: python scrape.py

The goal of this script is to have a way to search through ALL text content on my blog,
including tags, comments, quotes, and titles, not just through specific tags or by scrolling through the archive.

Loosely based on https://first-web-scraper.readthedocs.io/en/latest/

Edge cases:
'it', 'an', 'a', 'the'

Input options:
search for multiple words appearing in the same post (order irrelevant)
// 'downloaded' flag should prevent the request call and instead search a 
	pre-processed dataset that was already downloaded (but therefore doesn't include the newest posts)
// 'short-circuit' flag should quit looking when the provided argument (number) of matches has been found
// -q quiet: don't print full text
// -u update: finds and adds newest posts to data set
// ordered phrases somehow

Returns:
(clickable?) links to all possible posts it could be

I should really be using python3 for this, but 'import requests' failed.

DATA STORAGE:

dictionary:
keyword : [postID1, postID2...]

second dictionary:
postID : ( full text ) // make the object a class eventually

DOWNLOAD STAGE:

download the first 1 pages and add the content as described above. (later, 400 pages)

SEARCH PHASE:

1. lookup all keywords
2. intersection of return sets
3. get more details
4. return links + full text



boy......is this html hard to parse lmao
i need a filterable attribute on the tag objects that get returned by beautifulSoup. does....anyone have that

