import nltk

class NGramCharacterModel:
    """
    N-gram character model

    Attributes:
        corpus: str
            Corpus used for training the n-gram model, concatenated into a single string
        n: int
            Specifies the length of the n-gram
        char_set: list(str)
            List of characters found in the corpus
        ngram_freq: nltk.ConditionalFreqDist
            Conditional frequency distribution of each character in char_set based on previous n-1 characters
    """
    def __init__(self, corpus, n, char_set):

        self.n = n
        self.char_set = char_set

        # Obtain n-grams from the training corpus and compute the conditional frequency distributions
        ngrams = nltk.ngrams(corpus, n)
        ngram_tuples = list(zip(*ngrams))
        prev_chars = list(zip(*ngram_tuples[:-1]))
        curr_chars = ngram_tuples[-1]

        self.ngram_freq = nltk.ConditionalFreqDist(list(zip(prev_chars, curr_chars)))

    def get_conditional_freqs(self, prev_chars):
        """
        Get the probability of each character in char_set given prev_chars

        Arguments:
            prev_chars: list(str)
                List of n-1 previous chars

        Returns:
            freqs: dict(char: float)
                Conditional frequencies for each character
        """
        if len(prev_chars) != self.n - 1:
            raise ValueError(f"prev_chars must contain {self.n - 1} characters")

        conditional_freqs = self.ngram_freq[prev_chars]
        freqs = {}
        for c in self.char_set:
            freqs[c] = conditional_freqs.freq(c)

        return freqs
