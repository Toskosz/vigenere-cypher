import re
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def clean_string(text):
    # Remove numbers and special characters
    text = re.sub('[^A-Za-z]+', ' ', text)

    # Remove punctuation
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for char in text:
        if char in punctuations:
            text = text.replace(char, '')

    # Remove whitespaces
    text = ''.join(text.split())

    return text