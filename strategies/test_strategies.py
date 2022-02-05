from typing import Set

from nltk.corpus import wordnet2021, brown

from strategies.gather_info import GatherInfo
from strategies.rank_order import RankOrder
from strategies.strategy import Strategy


def main(words: Set[str], length: int):

    guess_limit = 6
    with open("previous_wordles.txt", "r") as file:
        previous_wordles = [line.strip().lower() for line in file.readlines()]
    number_previous = len(previous_wordles)
    missing_words = [w for w in previous_wordles if w not in words]
    print(f"Your dictionary is missing {len(missing_words)} words. \n\t{', '.join(missing_words)}\n")

    rank = RankOrder(dictionary=words, word_length=length, guess_limit=guess_limit)
    rank_score = rank.score_strategy(previous_wordles)
    rank_average = (guess_limit + 1) - (rank_score / number_previous)

    gather = GatherInfo(dictionary=words, word_length=length, guess_limit=guess_limit, gather_turns=2)
    gather_score = gather.score_strategy(previous_wordles)
    gather_average = (guess_limit + 1) - (gather_score / number_previous)

    print(f"Rank Order score: {rank_score}. Guesses correct wordle on try {round(rank_average, 2)} on average.")
    print(f"Gather Info score: {gather_score}. Guesses correct wordle on try {round(gather_average, 2)} on average.")


if __name__ == '__main__':
    word_soup = set()

    word_length = 5
    wordnet: Set[str] = Strategy.process_dictionary(set(wordnet2021.words()), word_length)
    brown: Set[str] = Strategy.process_dictionary(set(brown.words()), word_length)

    word_soup.update(wordnet)
    word_soup.update(brown)

    main(word_soup, word_length)
