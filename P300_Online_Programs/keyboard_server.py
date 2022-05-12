import pickle
import socketserver
import string

from functools import partial
from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel

from ngram import NGramCharacterModel
from nltk.corpus import brown
from word_recommender import WordRecommender

class KeyboardHandler(socketserver.StreamRequestHandler):
    """
    Request handler class for server. 
    """

    def __init__(self, word_recommender, ngram_model, *args, **kwargs):
        self.word_recommender = word_recommender
        self.ngram_model = ngram_model

        super().__init__(*args, **kwargs)

    def handle(self):
        keyboard_data = pickle.load(self.rfile)

        curr_text = keyboard_data.curr_text
        keyboard_data.word_suggestions = self.word_recommender.predict_next_word(curr_text, 5)

        ngram_length = self.ngram_model.length
        if len(curr_text) >= ngram_length - 1:
            prev_chars = tuple(curr_text[-(ngram_length-1):])
            keyboard_data.char_probs = self.ngram_model.get_conditional_freqs(prev_chars)

        pickle.dump(keyboard_data, self.wfile)

def main():
    HOST, PORT = 'localhost', 9999

    print("Begin init")

    model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    word_recommender = WordRecommender(model, tokenizer)

    corpus = ' '.join(brown.words()).lower()
    ngram_model = NGramCharacterModel(corpus, 3, list(string.ascii_lowercase + ' '))

    # Required due to how the RequestHandler is designed in Python
    handler = partial(KeyboardHandler, word_recommender, ngram_model)

    print("Done!")

    with socketserver.TCPServer((HOST, PORT), handler) as server:
        server.serve_forever()

    
if __name__ == "__main__":
    main()
