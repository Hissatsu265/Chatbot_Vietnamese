from underthesea import text_normalize, word_tokenize, sent_tokenize

def preprocess_text(text: str) -> list[str]:
    normalized = text_normalize(text)
    sentences = sent_tokenize(normalized)
    print(sentences)
    return [" ".join(word_tokenize(sent, format="text").split()) for sent in sentences]
