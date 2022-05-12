from dataclasses import dataclass, field

@dataclass
class KeyboardDto:
    curr_text: str
    word_suggestions: list[str] = field(default_factory=list)
    char_probs: dict = field(default_factory=dict)

    def __getitem__(self, item):
        return getattr(self, item)
