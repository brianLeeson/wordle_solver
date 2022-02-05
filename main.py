from typing import Set

from nltk.corpus import brown, wordnet2021

from strategies.gather_info import GatherInfo
from strategies.strategy import Strategy

"""
In addition to having nltk installed, you must first run this file
import nltk
nltk.download()
"""


def main(words: Set[str], length: int):
    strategy = GatherInfo(dictionary=words, word_length=length, guess_limit=6, gather_turns=2)
    strategy.play()


if __name__ == '__main__':
    word_soup = set()

    word_length = 5
    wordnet: Set[str] = Strategy.process_dictionary(set(wordnet2021.words()), word_length)
    brown: Set[str] = Strategy.process_dictionary(set(brown.words()), word_length)

    word_soup.update(wordnet)
    word_soup.update(brown)

    main(word_soup, word_length)

