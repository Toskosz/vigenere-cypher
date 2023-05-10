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
        self.samples = []
        self.key_size = 0
        self.char_frequency = self.get_char_frequency(language)
        self.get_key_size(cipherText.upper())
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

    def get_key_size(self, ciphertext):
        size = 0

        # 1000 arbitrario
        while size < 1000:
            size += 1
            samples = [''] * size
            
            for i in range(len(ciphertext)):
                samples[i % size] += ciphertext[i]
            
            sum = 0
            for i in range(size):
                sum += self.index_of_coincidence(samples[i])
            
            ioc = sum / size
            if ioc > 1.6:
                self.key_size = size
                self.samples = samples
                return

    def inner_dot_product(self,language_freq, sample_frequency):
        numerator = 0
        language_freq_magnitude = 0
        sample_freq_magnitude = 0

        for i in range(len(language_freq)):
            numerator += language_freq[i] * sample_frequency[i]
            language_freq_magnitude += language_freq[i] * language_freq[i]
            sample_freq_magnitude += sample_frequency[i] * sample_frequency[i]
        
        return numerator / sqrt(language_freq_magnitude * sample_freq_magnitude)

    def crack(self, ciphertext):
        frequencies = []
        for i in range(self.key_size):
            frequencies.append([0]*26)

            # char freq on sample
            for j in range(len(self.samples[i])):
                frequencies[i][ALPHABET.index(self.samples[i][j])] += 1
            for j in range(26):
                frequencies[i][j] = frequencies[i][j] / len(self.samples[i])
        
        key = ['A'] * self.key_size
        
        for i in range(self.key_size):
            for j in range(26):
                testtable = frequencies[i][j:]+frequencies[i][:j]
                if self.inner_dot_product(self.char_frequency,testtable) > 0.9:
                    key[i] = ALPHABET[j]
        plaintext = Vigenere.decrypt(ciphertext,key)

        print(f'Key: {"".join(key)}')
        print(f'Mensgem:\n{plaintext}')