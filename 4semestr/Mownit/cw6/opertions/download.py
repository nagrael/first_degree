from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_metadata
import os


def download():
    """
    ściąga dokumenty
    :return:
    """
    for i in range(1, 3000):
        try:
            query = strip_headers(load_etext(i)).strip()
        except Exception:
            continue
        if 'DOCTYPE HTML PUBLIC' not in query[0:100]:
            a = ''.join(get_metadata('title', 2701))
            with open('files/'+a+'.txt','a') as f:
                try:
                    f.write(query)
                    print('Downloaded ' +a +'.\n')
                except UnicodeEncodeError:
                    f.close()
                    os.remove('files/'+a+'.txt')
                    continue

        else:
            print("Not Downloaded")
			
download()