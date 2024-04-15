import pickle
import os
from search.scraper import Saver, Scraper
from pytest import approx


def write_pickle_obj(obj, filepath):
    with open(filepath, "wb") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def write_test_data(test_data_path):
    words_to_ids = {"cat": [1, 2], "dog": [3]}
    write_pickle_obj(words_to_ids, os.path.join(test_data_path, "words_to_ids.pkl"))
    return words_to_ids

def test_instantiate_scraper():
    url = "www.google.com"
    scraper = Scraper(url)
    assert scraper.url == url
    assert scraper.url is url

def test_load_files_successfully(tmp_path):
    saver = Saver(target_dir=tmp_path, name="words_to_ids")
    write_test_data(tmp_path)
    saver.load()
    assert saver.item["cat"] == [1, 2]

def test_wont_load_nonexistent_files(tmp_path):
    orig_val = {"squirrel": [3]}
    saver = Saver(target_dir=tmp_path, item=orig_val, name="words_to_ids")
    saver.load()
    assert type(saver.item) == dict
    assert saver.item == orig_val

def test_modify_save_and_reload_successfully(tmp_path):
    saver = Saver(target_dir=tmp_path, item={}, name="test")
    saver.item["ferret"] = [4]
    orig_val = saver.item
    saver.save()
    saver.load()
    assert saver.item["ferret"] == [4]
    assert orig_val is not saver.item
