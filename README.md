# Word Cloud generator
Generate word cloud diagrams from plain text files. This script have a few options for you to customize your word cloud diagrams, if you want a full customization dig into the code of this script and change the WordCloud function from the wordcloud Python library. 
The sript not only works with a single text file, it has a recursive option to create word clouds diagrams from a directory full of plain text files.
It supports Windows and Unix OS.

## Usage
Here is an example of how you can run this script:
```
>> python script.py -f .\\Path\\To\\File.txt -r \\Path\\To\\Directory\\ -s .\\Path\\To\\StopwordsFile.txt -m .\\Path\\To\\Mask.jpg
```
## Flags
- -f -> Add path to a plain text file
- -d -> Add path to a directory with plain text files
- -r -> Add the path where you are going to store the WordCloud images
- -m -> Mask of th WordCloud (shape)
- -s -> List of words you want to exclude from the WordCloud
## Recommendations
- Use double backslash to write the paths if you are on Windows OS `\\`
- The stopwords.txt file is recommended to be in list form
- Download all the Python dependencies and libraries before running the script
