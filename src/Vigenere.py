from utils import *

class Vigenere:

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @staticmethod
    def encrypt(plain_text, key):
        plain_text = plain_text.upper()
        key = key.upper()

        ciphertext = ''
        for i in range(len(plain_text)):
            p = ALPHABET.index(plain_text[i])
            k = ALPHABET.index(key[i%len(key)])
            c = (p + k) % 26
            ciphertext += ALPHABET[c]
        return ciphertext

    @staticmethod
    def decrypt(ciphertext,key):
        plaintext = ''
        for i in range(len(ciphertext)):
            p = ALPHABET.index(ciphertext[i])
            k = ALPHABET.index(key[i%len(key)])
            c = (p - k) % 26
            plaintext += ALPHABET[c]
        return plaintext