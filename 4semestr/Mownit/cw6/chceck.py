from opertions.find import finder, finder_svd, finder_svd_nonorm
from opertions.prepare import preapare_to_usage, to_svd
from opertions.matrix_do import union_words, do_matrix


def main():
    #union_words()
    #do_matrix()
    #preapare_to_usage()
    #to_svd()

    s = """his sacrifice bless
    """
    finder(s)
    finder(s, idf=False)
    finder_svd(s)


if(__name__ == "__main__"):
    main()

