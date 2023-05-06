from Crack import VigenereCrack
from utils import clean_string
import sys

def run():
    desired_challenge = sys.argv[1];
    if desired_challenge.lower() == "desafio1":
        cipherText = clean_string(open("challenges/desafio1.txt", "r").read())
        VigenereCrack(cipherText, language="english")
    else:
        cipherText = clean_string(open("challenges/desafio2.txt", "r").read())
        VigenereCrack(cipherText, language="portuguese")


if __name__ == "__main__":
    run()