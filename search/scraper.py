from argparse import ArgumentParser
import pickle
import requests
import os
import sys

class Searcher():

    def __init__(self):
        self.words_to_ids = {}
        self.ids_to_text = {}

class Saver():
    
    def __init__(self, target_dir=".", item=None, name=""):
        self.target_dir = target_dir
        self.item = item
        self.name = name

    def complete_path(self):
        return os.path.join(self.target_dir, f"{self.name}.pkl")

    def load(self):
        self.item = self.return_if_not_none(self.load_obj(), default=self.item)

    def load_obj(self):
        filepath = self.complete_path()
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                return pickle.load(f)

    def save(self):
        with open(self.complete_path(), "wb") as f:
            pickle.dump(self.item, f, pickle.HIGHEST_PROTOCOL)

    def return_if_not_none(self, new_value, default=None):
        if new_value:
            return new_value
        return default
    
    def clear(self):
        self.item = None
        self.save()

            
class Scraper:

    def __init__(self, url: str, saver: Saver=None):
        self.url = url
        self.saver = saver if saver else Saver()

    def download_pages(self, num_pages, start_page=1):
        contents = []
        for i in range(num_pages):
            page = start_page + i
            print(f"downloading page {page}...")
            page_url = self.url + "/page/" + str(i)
            response = requests.get(page_url)
            html = response.content
            contents.append(html)

def current_target_dir():
    package_path, _ = os.path.split(__file__)
    return package_path

def create_cli_parser():
    parser = ArgumentParser(prog="scrape.py", description="scrape data from a tumblr url", epilog="test")
    parser.add_argument("-n", "--num_pages", type=int)
    parser.add_argument("-f", "--fresh", action="store_true")
    return parser

def main():
    my_url = "https://johnlacena.tumblr.com"
    obj_dir = os.path.join(current_target_dir(), "obj")
    saver = Saver(target_dir=obj_dir)
    saver.load()
    scraper = Scraper(url=my_url, saver=saver)

    args = create_cli_parser().parse_args()
    print(f"{args.num_pages =}, {args.fresh =}")

    if args.fresh:
        print("clearing data.")
        scraper.saver.clear()

    if args.num_pages:
        scraper.download_pages(args.num_pages)

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