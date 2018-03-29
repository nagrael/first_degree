import os
import pickle
from opertions.word_checking import *
from collections import Counter


def union_words():
    """
    Tworzy zbiór termów z dokumentów
    :return:
    """
    union_set = set()
    for name in os.listdir('./files'):
        if os.path.isfile('./files/' + name):
            with open('files/'+name) as f:
                query = f.read()
        try:
            tmp_set = set(to_word_list(query))
        except ValueError:
            print("Wrong first 5000 words: " + name)
            continue
        union_set = union_set | tmp_set
        print((len(tmp_set)), len(union_set))

    with open('usage_files/union.txt', 'wb') as f:
        pickle.dump(list(union_set), f)


def do_matrix():
    """
    Tworzy macierz częstości występowania słów ze zbioru
    w poszczegolnych dokumentach
    :return:
    """
    with open('usage_files/union.txt', 'rb') as f:
        item_list = list(pickle.load(f))
    name_list = []
    all_vectors = []
    for name in os.listdir('./files'):
        if os.path.isfile('./files/' + name):
            with open('files/' + name) as f:
                query = f.read()
            try:
                tmp_count = Counter(to_word_list(query))
            except ValueError:
                print("Wrong first 5000 words: " + name)
                continue
            print('File ' + name)
            name_list.append(name)
            all_vectors.append([tmp_count[x] for x in item_list])

    with open('usage_files/matrix.txt', 'wb') as f:
        pickle.dump(all_vectors, f)
    with open('usage_files/name.txt', 'wb') as f:
        pickle.dump(name_list, f)
