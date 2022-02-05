from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Set


class Strategy(ABC):
    def __init__(self, dictionary: Set[str], word_length: int, guess_limit: int):
        # ensure no duplicates and use only correct length words
        self.dictionary = self.process_dictionary(dictionary, word_length)
        self.length = word_length
        self.guess_limit = guess_limit

    @abstractmethod
    def play(self, known_word: str = "") -> int:
        """
        Play wordle. If no known_word is given ask for input, if known_word is given play automatically
        :param known_word: the answer to the wordle if it is known beforehand. Used for scoring
        :return: The score. 0 for couldn't guess, guess_limit for first try, guess_limit-1 for second try, ...
        """
        pass

    @staticmethod
    def get_letter_frequency(words_to_survey: List[str], length: int) -> List[Dict[str, int]]:
        """
        :return: letter frequency per position
        """
        frequency_survey = [dict() for _ in range(length)]  # [{letter: count}, {letter: count}, ...]
        for word in words_to_survey:
            for position, letter in enumerate(word):
                if letter not in frequency_survey[position]:
                    frequency_survey[position][letter] = 1
                frequency_survey[position][letter] += 1

        return frequency_survey

    @staticmethod
    def rank_words(words_to_rank: List[str], letter_rankings: List[Dict[str, int]]) -> List[str]:
        """
        :return: ranked words by letter_rankings
        """
        ranked_words: Dict[str, int] = {}  # {word: score}
        for word in words_to_rank:
            score = 0
            for position, letter in enumerate(word):
                score += letter_rankings[position][letter]

            ranked_words[word] = score

        sorted_ranked_words = sorted(ranked_words.items(), key=lambda x: x[1], reverse=True)
        sorted_ranked_words = [word[0] for word in sorted_ranked_words]
        return sorted_ranked_words

    def score_strategy(self, words: List[str]) -> int:
        """
        :return: the score for the strategy for the given words. higher the score, the better the strategies
        """
        score = 0
        for word in words:
            score += self.play(known_word=word)

        return score

    @staticmethod
    def process_dictionary(dictionary: Set[str], word_length: int) -> Set[str]:
        """
        :return: a processed dictionary without duplicates and with words of the correct length
        """
        processed = set([w.lower() for w in dictionary if len(w) == word_length and w.isalpha()])
        return processed
