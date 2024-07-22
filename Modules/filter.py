
def clean_string(text: str, removable_words : list | None  = None) -> str:
    text = text.lower()
    removable_chars = list('.,:;()/¿?!¡%$&_-@1234567890') # Add or remove special characters
    spanish_accents = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u'} # Add or remove special accents
    #--------------------------------#
    for accent in spanish_accents:
        text = text.replace(accent, spanish_accents[accent])
    #--------------------------------#
    for char in removable_chars:
        text = text.replace(char, '')
    #--------------------------------#
    text = text.split()

    if removable_words != None:
        for word in removable_words:
            while word in text:
                text.remove(word)
    #--------------------------------#
    string = ''
    for word in text:
        string += word + ' '
    string = string[:-1]
    return string


if __name__=='__main__':
    print('This file is a module of the Word Cloud generator script. Execute the Word Cloud generator script to use this function.')