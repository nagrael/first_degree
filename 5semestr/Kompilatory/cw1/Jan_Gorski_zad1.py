import os
import sys
import re
import codecs
#REGEX_START

sentence_end_regex = re.compile(r'([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z](\.|!|\?)+\b|(<.+?>)+\n)')

cutoff_regex = re.compile(r'(?:^|(?<=\s))([a-zA-Z]|[a-zA-Z]{2}|[a-zA-Z]{3})\.(?=$|\s)')

email_regex = re.compile(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.([a-zA-Z0-9-].)*[a-zA-Z0-9-])')

positive_integer = r'[1-2][0-9]{4}|3[0-1][0-9]{3}|32[0-6][0-9]{2}|3276[0-7]|327[0-5][0-9]|[1-9][0-9]{0,3}'

negative_integer = r'-32768|-({0})'.format(positive_integer)

integer_regex = re.compile(r'(?:^|(?<=\s))({0}|{1}|0)(?=$|\s)'.format(positive_integer, negative_integer))

floa_regex = re.compile(r'(?:^|(?<=\s))-?([0-9]+\.[0-9]*|\.[0-9]+|[0-9].[0-9][eE][+-][0-9]+)(?=$|\s)')

separators = [r'\.', r'-', r'/']

max_month_day = \
    [(1, 31), (2, 29), (3, 31), (4, 30), (5, 31), (6, 30), (7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31)]

#Date because there are many possibilities
def date_regex():
    def number_to_regex(number):
        if (number < 10):
            return r'(0[0-{0}])'.format(number)
        else:
            return r'(?:(?:{0}[0-{1}])|(?:[0-{2}][0-9]))'.format(str(number)[0], str(number)[1], str(number-10)[0])
    result = []
    for separator in separators:
        for month, max_day in max_month_day:
            result.append( r'{2}{0}{1}{0}{3}|{3}{0}{1}{0}{2}'\
                .format(separator, number_to_regex(month), number_to_regex(max_day), '[0-9]{4}'))
            # format and day for different months

    return re.compile('|'.join(result))

#REGEX_END

def generate_meta_regexp(type_):
    return re.compile('<META NAME="' + type_ + '" CONTENT="(.+)">')

def get_meta_content(content):
    return '\n'.join(re.compile('^<META NAME.+$', re.MULTILINE).findall(content))

def get_non_meta_content(content):
    return ''.join(re.compile(r'<P[\s\S]*?(?=<META NAME=)', re.MULTILINE).findall(content))

def process_file(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()

    meta_content = get_meta_content(content)
    authors = generate_meta_regexp('AUTOR').findall(meta_content)
    dzial = generate_meta_regexp('DZIAL').findall(meta_content)
    key_words = generate_meta_regexp(r'KLUCZOWE_[0-9]').findall(meta_content)

    content = get_non_meta_content(content)
    sentences = sentence_end_regex.findall(content)
    cutoffs = cutoff_regex.findall(content)
    integers = integer_regex.findall(content)
    float_numbers = floa_regex.findall(content)
    dates = date_regex().findall(content)
    emails = email_regex.findall(content)

    fp.close()
    print("nazwa pliku: " + filepath)
    print("autor: " + ', '.join(authors))
    print("dzial: " + ', '.join(dzial) )
    print("slowa kluczowe: " + ', '.join(key_words))
    print("liczba zdan: " + str(len(sentences)))
    print("liczba skrotow: " + str(len(cutoffs)))
    print("liczba liczb calkowitych z zakresu int: " + str(len(integers)))
    print("liczba liczb zmiennoprzecinkowych: " + str(len(float_numbers)) )
    print("liczba dat: " + str(len(dates)))
    print("liczba adresow email: " + str(len(emails)))
    print("\n")

try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)
tree = os.walk(path)
for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            process_file(filepath)