# text-search


install:

    ./env.sh
    source ./virtualenv/bin/activate
    pip3 install -r requirements.txt

usage:

    python3 search/scraper.py

tests:

    pytest

The goal of this script is to have a way to search through text content retrieved from various web apis.


For example, thinking about tumblr, it would be convenient to search through all text content of one blog,
including tags, comments, quotes, and titles, not just through specific tags or by scrolling through the archive.


Another example would be searching a user's spotify playlists for a song, based only on <em>fragments</em> of a title, artist, or album name.

HTML processing loosely based on https://first-web-scraper.readthedocs.io/en/latest/

Future goal: enable fuzzy matching by building a graph of words connected by edit distance.

Input options:

     -f --fresh         # clear out and refresh data (takes time)
     -n --num_pages     # number of pages/batches to download



Returns:
clickable links to results

DATA STORAGE:

    dictionary:
    keyword : [postID1, postID2...]

    second dictionary:
    postID : (Object)


// DEPRECATED //

Input options:
search for multiple words appearing in the same post (order irrelevant)
// 'downloaded' flag should prevent the request call and instead search a 
	pre-processed dataset that was already downloaded (but therefore doesn't include the newest posts)
// 'short-circuit' flag should quit looking when the provided argument (number) of matches has been found
// -q quiet: don't print full text
// -u update: finds and adds newest posts to data set
// ordered phrases somehow


SEARCH:

1. lookup all keywords
2. intersection (or union, based on arguments) of return sets
3. return links + post text
