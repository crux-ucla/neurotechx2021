import torch

class WordRecommender:
    """
    Word recommendation system

    Attributes:
        model: torch.nn.Module
            Neural language model used to predict words
        tokenizer: transformers.Tokenizer
            Used to encode/decode input/output for model
    """
    def __init__(self, model, tokenizer):

        self.model = model
        self.tokenizer = tokenizer

    def predict_next_word(self, text, num_words=3):
        """
        Predicts the next word. If last character typed was a space, predicts the next 
        word. Otherwise, predicts the current word being typed like an autocomplete system.

        Arguments:
            text: str
                Text to predict the current/next word for
            num_words: int
                Number of words to suggest
            reject_words: list(str)
                Block list for predicted words
        
        Returns:
            word_suggestions: list(str)
                List of most likely words based on text
        """
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

        tokens = torch.tensor([self.tokenizer.encode(prev_text)])
        # Set model to evaluation mode and predict
        self.model.eval()

        with torch.no_grad():
            outputs = self.model(tokens)
            predictions = outputs[0]

        probs = predictions[0, -1, :]
        pred_indices = torch.argsort(probs, descending=True)

        word_suggestions = set()
        for idx in pred_indices:
            word = self.tokenizer.decode(idx.item()).strip()
            if word.startswith(next_word_substr) and word.isalpha():
                word_suggestions.add(word.lower())

            if len(word_suggestions) == num_words:
                break

        return list(word_suggestions)
