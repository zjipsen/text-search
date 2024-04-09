from argparse import ArgumentParser
import pickle
import requests


class Scraper():
    
    def __init__(self, url):
        self.url = url
        self.obj_path = "./obj/"
        self.load()

    def load(self):
        self.words_to_ids = self.load_obj("words_to_ids")
        self.ids_to_text = self.load_obj("ids_to_text")

    def clear(self):
        self.words_to_ids = {}
        self.ids_to_text = {}
        self.save_obj(self.words_to_ids, "words_to_ids")
        self.save_obj(self.ids_to_text, "ids_to_text")

    def load_obj(self, name):
        with open(self.obj_path + name + ".pkl", "rb") as f:
            return pickle.load(f)
        
    def save_obj(self, obj, name):
        with open(self.obj_path + name + ".pkl", "wb") as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
            
    def download_pages(self, num_pages, start_page=1):
        for i in range(num_pages):
            page = start_page + i
            print(f"downloading page {page}...")
            page_url = self.url + "/page/" + str(i)
            response = requests.get(page_url)
            html = response.content

def main():
    my_url = "https://johnlacena.tumblr.com"
    scraper = Scraper(url=my_url)

    parser = ArgumentParser(prog="scrape.py", description="scrape data from a tumblr url", epilog="test")
    parser.add_argument("-n", "--num_pages", type=int)
    parser.add_argument("-f", "--fresh", action="store_true")
    args = parser.parse_args()
    print(f"{args.num_pages =}, {args.fresh =}")

    if args.fresh:
        print("clearing data.")
        scraper.clear()

    if args.num_pages:
        scraper.download_pages(args.num_pages)

    print(len(scraper.ids_to_text.keys()))
    # for id in scraper.ids_to_text.keys():
    #     print(f"{id=}")
    #     print(f"{scraper.ids_to_text[id]}")
        
    # download_content(100)
    query = "phenomenon"
    # search_results = search_union(query)
    # print(search_results if (search_results) else "No results found for the query \"" + str(query) + "\"")
    # save_dictionaries()


if __name__ == '__main__':
    main()