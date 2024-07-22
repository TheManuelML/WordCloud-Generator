import os
import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud
from Modules.filter import clean_string

# Arguments
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-d', '--dir')
parser.add_argument('-f', '--file')
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
    wc = WordCloud(
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
## Recursive function to create WordClouds 
def recursive(dir_path : str, wordcloud_path : str, mask : str | None = None, stopwords : list | None = None) -> None:
    with os.scandir(dir_path) as files:
        for txt in files:
            if txt.is_file():
                wc_name = txt.name[:-4] + '.png'
                txt_path = os.path.join(dir_path, txt.name)
                wc_path = os.path.join(wordcloud_path, wc_name)
                # From txt to string
                text = txt_to_string(txt_path)
                # Creating Word Cloud
                wordcloud(text, wc_path, mask, stopwords)
    return None

## Single function to create WordCloud
def single(file_path : str, wordcloud_path : str, mask : str | None = None, stopwords : list | None = None) -> None:
    txt_name = os.path.basename(file_path)
    wc_name = txt_name[:-4] + '.png'
    txt_path = file_path
    wc_path = os.path.join(wordcloud_path, wc_name)
    # From txt to string
    text = txt_to_string(txt_path)
    # Creating Word Cloud
    wordcloud(text, wc_path, mask, stopwords)
    return None

# Main function
def main() -> None:
    ## Results path
    if argument.results:
        wordcloud_path = argument.results
    else:
        print('The results directory path is required!!!')
        sys.exit(1)
    #------------------------------------------------------------#
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
    #------------------------------------------------------------#
    ## Directory and file path
    if argument.dir and argument.file:
        print('Choose between a directory or a file path!!!')
        sys.exit(1)
    elif argument.dir:
        dir_path = argument.dir
        recursive(dir_path, wordcloud_path, wc_mask, stopwords)
    elif argument.file:
        file_path = argument.file
        single(file_path, wordcloud_path, wc_mask, stopwords)
    else:
        print('The directory or file parameter is required!!!')
        sys.exit(1)
    return None


if __name__=='__main__':
    main()
