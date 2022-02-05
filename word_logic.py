from typing import List, Set


class WordLogic:
    def __init__(self, word_length: int):
        self.word_length = word_length

        self.green_position: List[str] = ["" for _ in range(self.word_length)]
        self.yellow_position: List[List[str]] = [[] for _ in range(self.word_length)]
        self.grey: Set[str] = set()

    def is_word_allowed(self, word: str) -> bool:
        """
        :return: True if the given word can be guessed
        """
        green_in_position = all([l in word[i] for i, l in enumerate(self.green_position)])
        has_yellow = all([letter in word for li in self.yellow_position for letter in li])
        yellow_in_wrong_position = any([word[i] in l for i, l in enumerate(self.yellow_position)])
        has_grey = not self.grey.isdisjoint(word)
        word_allowed = green_in_position and has_yellow and not yellow_in_wrong_position and not has_grey

        return word_allowed

    def is_word_unique(self, word: str) -> bool:
        """
        :return: True if the word does not contain green, yellow, or grey letters or duplicates
        """
        no_green = all([letter not in word for letter in self.green_position if letter != ""])
        no_yellow = all([letter not in word for li in self.yellow_position for letter in li])
        no_grey = all([letter not in word for letter in self.grey])
        no_duplicates = len(word) == len(set(word))

        return no_green and no_yellow and no_grey and no_duplicates

    def update(self, green: str, yellow: str, guessed_word: str) -> None:
        """
        update the internal data sets after a word has been guess
        :param green: the integer positions as strings of the green boxes EX: "134"
        :param yellow: the integer positions as strings of the yellow boxes EX: "134"
        :param guessed_word: the word that was just guessed
        :return: None
        """
        grey_letters = set([letter for letter in guessed_word])

        for position in green[:self.word_length]:
            position = int(position)
            letter = guessed_word[position]
            self.green_position[position] = letter
            if letter in grey_letters:
                grey_letters.remove(letter)

        for position in yellow[:self.word_length]:
            position = int(position)
            letter = guessed_word[position]
            self.yellow_position[position].append(letter)
            if letter in grey_letters:
                grey_letters.remove(letter)

        self.grey.update(grey_letters)

    def update_known(self, guessed_word: str, known_word: str) -> None:
        """
        if the answer word in known, used instead of update and will automatically determine the color positions
        :param guessed_word: the word that was just guessed
        :param known_word: the wordle answer
        :return: None
        """
        green = ""
        yellow = ""

        for position, letter in enumerate(guessed_word):
            letter_position_match = letter == known_word[position]
            if letter_position_match:
                green += str(position)
            elif letter in known_word:
                yellow += str(position)

        self.update(green, yellow, guessed_word)
