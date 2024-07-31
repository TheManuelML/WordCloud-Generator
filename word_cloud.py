import os
import argparse
import os.path
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud
from Modules.filter import clean_string


# Arguments
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-p', '--path')
parser.add_argument('-r', '--results')
parser.add_argument('-m', '--mask')
parser.add_argument('-s', '--stopwords')
argument = parser.parse_args()


# Transform
## Text file to one string
def txt_to_string(file_path : str) -> str:
    text = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        for word in file:
            text += word
    filtered = clean_string(text)
    return filtered

## Stopwords text file to list
def stopwords_to_list(stopwords_path : str) -> list:
    with open(stopwords_path, 'r', encoding='utf-8') as file:
        stopwords = [line.strip() for line in file if line.strip()]
    return stopwords

## Create Word Cloud
def wordcloud(text : str, wordcloud_path : str, mask : str | None = None, stopwords : list | None = None) -> None:
    wc = WordCloud( # Add more parameters if you want
        background_color = 'white', 
        max_words = 100, # Change this
        min_font_size = 8, # Change this
        mask = mask,
        stopwords = stopwords
    ).generate(text)
    plt.axis('off')
    plt.imshow(wc, interpolation='bilinear')
    plt.savefig(wordcloud_path)
    plt.close()
    return None


# File and recursive functions
## File processing
def file_processing(file_path : str, wordcloud_path : str, mask : str | None = None, stopwords : list | None = None) -> None:
    txt_name = os.path.basename(file_path)
    wc_name = txt_name[:-4] + '.jpg'
    wc_path = os.path.join(wordcloud_path, wc_name)

    text = txt_to_string(file_path)
    wordcloud(text, wc_path, mask, stopwords)
    return None

## Directory processing
def dir_processing(directory_path : str, wordcloud_path : str, mask : str | None = None, stopwords : list | None = None) -> None:
    with os.scandir(directory_path) as first_level:
        for element in first_level:
            if os.path.isdir(element.path):
                recursive(element.path, wordcloud_path, mask, stopwords)
            elif os.path.isfile(element.path) and element.name.endswith('.txt'):
                file_processing(element.path, wordcloud_path, mask, stopwords)
    return None

## Recursive
def recursive(directory_path : str, wordcloud_path : str, mask : str | None = None, stopwords : list | None = None) -> None:
    for element in os.listdir(directory_path):
        full_path = os.path.join(directory_path, element)
        if os.path.isdir(full_path):
            recursive(full_path, wordcloud_path, mask, stopwords)
        else:
            file_processing(full_path, wordcloud_path, mask, stopwords)
    return None


# Main function
def main() -> None:
    ## Results path
    if argument.results:
        wordcloud_path = argument.results
    else:
        print('The results directory path is required!!!')
        sys.exit(1)
    
    ## Mask  & Stopwords for the Word Cloud
    if argument.mask:
        wc_mask = np.array(Image.open(argument.mask))
    else:
        wc_mask = None
    
    if argument.stopwords:
        stpwrds_path = argument.stopwords
        stopwords = stopwords_to_list(stpwrds_path)
    else:
        stopwords = None
    
    ## Directory and file path
    if not argument.path:
        print('Path argument is necesary!!!')
        sys.exit(1)
    elif os.path.isdir(argument.path):
        dir_path = argument.path
        dir_processing(dir_path, wordcloud_path, wc_mask, stopwords)
    elif os.path.isfile(argument.path):
        file_path = argument.path
        file_processing(file_path, wordcloud_path, wc_mask, stopwords)
    else:
        print('Write a valid path!!!')
        sys.exit(1)
    return None


if __name__=='__main__':
    main()
