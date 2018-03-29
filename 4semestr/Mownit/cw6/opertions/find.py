import os
import pickle
from timeit import default_timer as timer
from collections import Counter
from numpy import array
from scipy.sparse import csr_matrix, csc_matrix
from scipy.sparse.linalg import norm
from opertions.word_checking import *
from opertions.prepare import load_sparse_csr, load_sparse_csc, normalized


def finder(s, idf=True):
    """
    Przetwarza zapytnie i wszukuje najlepiej pasujące
    :param s:String: zapytanie
    :param idf: Wyszukac przy wyorzystanie macierzy z idf
    :return: 10 nablizszych wyników
    """
    start = timer()
    with open('usage_files/union.txt', 'rb') as f:
        items = list(pickle.load(f))
    with open('usage_files/name.txt', 'rb') as f:
        name = list(pickle.load(f))
    try:
        text = Counter(to_word_list(s))
    except ValueError:
        raise
    q = [text[x] for x in items]
    q = csr_matrix(array(normalized(array(q))))
    if idf:
        newm = load_sparse_csr("usage_files/with_idf.npz")
    else:
        newm = load_sparse_csr("usage_files/without_idf.npz")
    after_q = timer()
    a = array(q.dot(newm).todense())[0].tolist()
    x = dict(zip(name, a))
    print(sorted(x.items(), reverse=True, key=lambda y: abs(y[1]))[:10])
    end = timer()
    print("Total time: " + str(end - start) + "\t Without load: " + str(end - after_q))


def finder_svd(s):
    """
    Przetwarza zapytnie i wszukuje najlepiej pasująceF
    Wykorzystuje macierze policzony przy użyciu SVD
    :param s:String zapytanie
    :return:
    """
    start = timer()
    with open('usage_files/union.txt', 'rb') as f:
        items = list(pickle.load(f))
    with open('usage_files/name.txt', 'rb') as f:
        name = list(pickle.load(f))
    try:
        text = Counter(to_word_list(s))
    except ValueError:
        raise
    q = [text[x] for x in items]
    q = csc_matrix(array(normalized(array(q))))
    for files in os.listdir('./svd'):
        if os.path.isfile('./svd/' + files):
            after_q = timer()
            newm = load_sparse_csc('svd/' + files)
            after_load = timer()
            print(files + " load time: " + str(after_load - after_q))
            a = array(q.dot(newm).todense())[0].tolist()
            x = dict(zip(name, a))
            print(sorted(x.items(), reverse=True, key=lambda y: abs(y[1]))[:10])
            end = timer()
            print(files + ": Time without load  " + str(end - after_load))
    end = timer()
    print("Total time: " + str(end - start))


def finder_svd_nonorm(s):
    """
    Przetwarza zapytnie i wszukuje najlepiej pasujące
    Wykorzystuje macierze policzony przy użyciu SVD bez normalizacji wczesniejszej
    :param s:String zapytanie
    :return:
    """
    start = timer()
    with open('usage_files/union.txt', 'rb') as f:
        items = list(pickle.load(f))
    with open('usage_files/name.txt', 'rb') as f:
        name = list(pickle.load(f))
    try:
        text = Counter(to_word_list(s))
    except ValueError as v:
        raise v
    q = [text[x] for x in items]
    q = csc_matrix(array(normalized(array(q))))
    for files in os.listdir('./svd'):
        if os.path.isfile('./svd/' + files):
            after_q = timer()
            newm = load_sparse_csc("svd/" + files)
            after_load = timer()
            print(files + " load time: " + str(after_load - after_q))
            di = dict()
            for j in range(len(name)):
                di[name[j]] = abs(norm_svd(newm.getcol(j), q))
            print(sorted(di.items(), reverse=True, key=lambda y: abs(y[1]))[:10])
            end = timer()
            print(files + " Time without load " + str(end - after_load))
    end = timer()
    print("Total time: " + str(end - start))


def norm_svd(di, q):
    """
    Oblicza norma miedzy di a q (q ma norme 1)
    :param di:
    :param q:
    :return:
    """
    a = norm(di)
    return ((q.dot(di) / a).toarray())[0][0]
