from bs4 import BeautifulSoup
from scrape import format_strings, find_all_text

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

run_tests()