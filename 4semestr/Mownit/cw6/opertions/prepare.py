import pickle
from scipy.sparse import lil_matrix, csr_matrix, diags, csc_matrix
from scipy.sparse.linalg import svds, norm
from numpy import log10, count_nonzero, matrix, array, linalg, savez, load


def normalized(v):
    norms = linalg.norm(v)
    if norms == 0:
        raise ZeroDivisionError("Norm is equal to 0!")
    return v / norms


def preapare_to_usage(with_idf=True):
    """
    Metoda przygotowuje macierz do użytku.
    Normalizuje oraz mnoży przez inverse document frequency
    :param with_idf: z użyciem inverse document frequency
    :return: zapisuje jako with_idf/without_idf
    """
    name = 'usage_files/without_idf'
    with open('usage_files/matrix.txt', 'rb') as f:
        item = pickle.load(f)
    with open('usage_files/union.txt', 'rb') as f:
        items = list(pickle.load(f))
    spare_matrix = array(item)
    if with_idf:
        name = 'usage_files/with_idf'
        x = [count_nonzero(spare_matrix[:, i]) for i in range(len(items))]
        x = [log10(len(item) / x[i]) if x[i] != 0 else 0 for i in range(len(x))]
        spare_matrix = (spare_matrix * array(x))
    x = array([[1 / linalg.norm(y)] for y in spare_matrix])
    spare_matrix = spare_matrix * x
    x = []
    spare_matrix = csc_matrix(lil_matrix(matrix(spare_matrix).getT()))
    save_sparse(name, spare_matrix)


def to_svd(beg=200, end=2613, jump=300, with_norm=True):
    """
        Wykonuje SVD na rzadkiej macierzy wczytanej z with_idf
    Zapisuej dla róznych wartosci k pod nazwa k, gdzie k = 1,2,3...A.shape-1 A-macierz

    :param beg: od ktorego k
    :param end:  do jakiego k
    :param jump: o jakie k
    :param with_norm: noramlizować przed zapisem
    :return: zapisuje macierze rzadkie do plikow
    """

    spare = load_sparse_csr('usage_files/with_idf.npz')
    x = []
    for k in range(beg, end, jump):
        print("Starting: " + str(k))
        U, sigma, V = svds(spare, k=k)
        print("Done svd")
        reconsign = csc_matrix(U) * diags(sigma, format='csc') * csc_matrix(V)
        print("Done multiplication")
        if with_norm:
            x = [(1 / norm(reconsign.getcol(i))) for i in range(reconsign.shape[1])]
            reconsign = reconsign.multiply(csc_matrix(x))
            x = []
        save_sparse('svd/' + str(k), csc_matrix(reconsign))
        print("Saved " + str(k))


def save_sparse(filename, array):
    """
    Zaisuje rzadką maciersz csr i csc
    :param filename: nazwa pliku do zapisu
    :param array: macierz do zapisu
    :return:
    """
    savez(file=filename, data=array.data, indices=array.indices,
          indptr=array.indptr, shape=array.shape)


def load_sparse_csr(filename):
    """
    Wczytuje macierz jako rzadka macierz csr
    :param filename: plik do odczytu
    :return:
    """
    loader = load(filename)
    return csr_matrix((loader['data'], loader['indices'], loader['indptr']),
                      shape=loader['shape'])


def load_sparse_csc(filename):
    """
    Wczytuje macierz jako rzadko macierz csc
    :param filename: plik do odczytu
    :return:
    """
    loader = load(filename)
    return csc_matrix((loader['data'], loader['indices'], loader['indptr']),
                      shape=loader['shape'])
