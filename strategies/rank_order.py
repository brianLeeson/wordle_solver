from strategies.strategy import Strategy
from word_logic import WordLogic


class RankOrder(Strategy):

    def play(self, known_word: str = "") -> int:
        """
        rank words in order of letter frequency and guess in that order, no tricks.
        :return the score based on number of guesses to correct answer
        """

        letter_frequency = self.get_letter_frequency(self.dictionary, self.length)
        ranked_words = self.rank_words(self.dictionary, letter_frequency)
        word_position_logic = WordLogic(self.length)

        for guess in range(self.guess_limit):
            # work your way down the list until you find a word that meets criteria and can be guessed
            for word in ranked_words:
                word_passes = word_position_logic.is_word_allowed(word)
                if not word_passes:
                    continue

                if known_word != "":
                    word_position_logic.update_known(guessed_word=word, known_word=known_word)
                    if word == known_word:
                        return self.guess_limit - guess
                    break

                # Guess and get input
                skipping = input(f"Your next guess is {word}. Press enter to confirm or 'skip' to skip\n") == 'skip'
                if skipping:
                    continue
                success = input("Did you guess right? y/n\n")
                if success == "y":
                    return self.guess_limit - guess
                elif word == ranked_words[-1]:  # all words skipped or guessed and failed
                    print("I've run out of words to guess. The word my not be in my dictionary")
                    return self.guess_limit - guess

                green_input = input(f"Enter the position (numbers 0-{self.length - 1}) of the green letters:\n")
                yellow_input = input(f"Enter the position (numbers 0-{self.length - 1}) of the yellow letters:\n")

                word_position_logic.update(green_input, yellow_input, word)
                break

        return 0

