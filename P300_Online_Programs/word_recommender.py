import torch
from pytorch_transformers importGPT2Tokenizer, GPT2LMHeadModel

class WordRecommender(model, tokenizer):
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def predict_next_word(text, num_words=3, reject_words=[]):
        prev_text, _, next_word_substr = text.rpartition(' ')

        if prev_text == '':
            # Still on first word, so predict based on the substring
            if next_word_substr != '':
                prev_text = next_word_substr
            # Nothing typed, predict on space to prevent error
            else:
                prev_text = ' '
        # Add space to prev_text to indicate that we are on next word
        else:
            prev_text += ' '

        tokens = torch.tensor([tokenizer.encode(prev_text)])
        # Set model to evaluation mode and predict
        model.eval()

        with torch.no_grad():
            outputs = model(tokens)
            predictions = outputs[0]

        probs = predictions[0, -1, :]
        pred_indices = torch.argsort(probs, descending=True)

        word_suggestions = set()
        for idx in pred_indices:
            word = tokenizer.decode(idx.item()).strip()
            if word.startswith(next_word_substr) and word not in reject_words:
                word_suggestions.add(word)

            if len(word_suggestions) == num_words:
                return word_suggestions

        return word_suggestions
