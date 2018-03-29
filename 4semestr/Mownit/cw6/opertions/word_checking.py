import string
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer


def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']


def using_translate(content):
    table = str.maketrans(
        string.punctuation,
        ' ' * len(string.punctuation))
    content = content.translate(table).lower()

    return content.split()[:5000]


def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return wn.NOUN


def to_word_list(query: str):
    """
    Tworzy ze stringa liste słów
    Słowa za zmienone przy pomocy NLTK
    Sprawdzany jest iloczyn słow ze słownikiem słow angielskich
    :param query: Dane do modyfikacji
    :return:
    """
    with open("usage_files/words.txt") as word_file:
        english_words = set(word.strip().lower() for word in word_file)
    tags = pos_tag((using_translate(query)))
    a = []
    for tag in tags:
        wn_tag = penn_to_wn(tag[1])
        word = WordNetLemmatizer().lemmatize(tag[0], wn_tag)
        if word.lower() in english_words:
            a.append(word)
    if len(a) == 0:
        raise ValueError("First 5000 words are not in english")
    return a
