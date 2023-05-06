from math import sqrt
from Vigenere import Vigenere
from utils import ALPHABET

class VigenereCrack:

    portuguese_frequency = [
        14.63,1.04,3.88,4.99,
        12.57,1.02,1.30,1.28,
        6.18,0.40,0.02,2.78,
        4.74,5.05,10.73,2.52,
        1.20,6.53,7.81,4.34,
        4.63,1.67,0.01,0.21,
        0.01,0.47]
    
    english_frequency = [
        8.167,1.492,2.782,4.253,
        12.702,2.228,2.015,6.094,
        6.966,0.153,0.772,4.025,
        2.406,6.749,7.507,1.929,
        0.095,5.987,6.327,9.056,
        2.758,0.978,2.360,0.150,
        1.974,0.074]

    def __init__(self, cipherText, language):
        self.slices = []
        self.period = 0
        self.char_frequency = self.get_char_frequency(language)
        self.get_period(cipherText.upper())
        self.crack(cipherText.upper())
        
    def get_char_frequency(self, language):
        if language == "english":
            return self.english_frequency
        elif language == "portuguese":
            return self.portuguese_frequency

    def index_of_coincidence(self, text):
        counts = [0]*26
        for char in text:
            counts[ALPHABET.index(char)] += 1
        numer = 0
        total = 0
        for i in range(26):
            numer += counts[i]*(counts[i]-1)
            total += counts[i]
        return 26*numer / (total*(total-1))

    def get_period(self, ciphertext):
        found = False
        period = 0

        while not found:
            period += 1
            slices = ['']*period
            for i in range(len(ciphertext)):
                slices[i%period] += ciphertext[i]
            sum = 0
            for i in range(period):
                sum += self.index_of_coincidence(slices[i])
            ioc = sum / period
            if ioc > 1.6:
                self.period = period
                self.slices = slices
                return

    def cosangle(self,x,y):
        numerator = 0
        lengthx2 = 0
        lengthy2 = 0
        for i in range(len(x)):
            numerator += x[i]*y[i]
            lengthx2 += x[i]*x[i]
            lengthy2 += y[i]*y[i]
        return numerator / sqrt(lengthx2*lengthy2)

    def crack(self, ciphertext):
        frequencies = []
        for i in range(self.period):
            frequencies.append([0]*26)
            for j in range(len(self.slices[i])):
                frequencies[i][ALPHABET.index(self.slices[i][j])] += 1
            for j in range(26):
                frequencies[i][j] = frequencies[i][j] / len(self.slices[i])
        key = ['A']*self.period
        for i in range(self.period):
            for j in range(26):
                testtable = frequencies[i][j:]+frequencies[i][:j]
                if self.cosangle(self.char_frequency,testtable) > 0.9:
                    key[i] = ALPHABET[j]
        plaintext = Vigenere.decrypt(ciphertext,key)
        print(plaintext)