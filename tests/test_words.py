import urllib.request

import glob
import pytest

DICIN_URL = "http://splasho.com/upgoer5/phpspellcheck/dictionaries/1000.dicin"

def download_list():
    text = urllib.request.urlopen(DICIN_URL).read()
    return text.decode().splitlines()

def remove_third(words_list, dictionary_list, check='s'):
    outwords = list()
    for word in words_list:
        check_word = word.lower()
        if check_word[-len(check):] == check and check_word[:-len(check)] in dictionary_list:
            outwords.append(word)
    for word in outwords:
        words_list.remove(word)
    return words_list

def analyse_text(text, dictionary_list):
    '''
    Inputs
    ------
    text: string containing the text to analyse

    dictionary_list: a list with all the allowed words

    '''
    text = text.replace(',','').replace('.','')
    badwords = [x for x in text.split() if x.lower() not in dictionary_list]
    for check in ['s', 'es', 'r']:
        if len(badwords) >  0:
            badwords = remove_third(badwords, dictionary_list, check)
    return badwords

def remove_comments(text):
    '''
    Inputs
    ------
    text: string list as from readlines
    '''
    final_text = ''
    #text = text.splitlines()
    for line in text:
        if line[0] != '#' and '//' not in line:
            final_text += line
    return final_text

def read_remove_analyse(filename, dictionary_list):
    with open(filename) as file_text:
        text = file_text.readlines()
    text = analyse_text(remove_comments(text), dictionary_list)
    return text

DICTIONARY_LIST = download_list()

DEFINITIONS = glob.glob('terms/**/*md', recursive=True)
@pytest.mark.parametrize('definition', DEFINITIONS)
def test_checkdefinition(definition):
    output = list()
    assert output == read_remove_analyse(definition, DICTIONARY_LIST)
