usage: python scrape.py

The goal of this script is to have a way to search through ALL text content on tumblr blogs,
including tags, comments, quotes, and titles, not just through specific tags or by scrolling through the archive.

Loosely based on https://first-web-scraper.readthedocs.io/en/latest/

Input options:
search for multiple words appearing in the same post (order irrelevant)
// 'downloaded' flag should prevent the request call and instead search a 
	pre-processed dataset that was already downloaded (but therefore doesn't include the newest posts)
// 'short-circuit' flag should quit looking when the provided argument (number) of matches has been found
// -q quiet: don't print full text
// -u update: finds and adds newest posts to data set
// ordered phrases somehow

Returns:
clickable links to all possible posts it could be

DATA STORAGE:

dictionary:
keyword : [postID1, postID2...]

second dictionary:
postID : ( full text ) // make the object a class eventually

SEARCH:

1. lookup all keywords
2. intersection (or union, based on arguments) of return sets
3. return links + post text
