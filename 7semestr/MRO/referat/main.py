from gensim.models import word2vec, ldamodel,ldamulticore
from gensim import corpora
import logging
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# p_stemmer = PorterStemmer()
# en_stop = get_stop_words('en')
# tokenizer = RegexpTokenizer(r'\w+')
# print("READ START!\n")
# file = open('text8', 'r')
# st = file.read()
# file.close()
# print("READ DONE!\n")
# tokens = tokenizer.tokenize(st)
#
# print("TOKENS!\n")
# stopped_tokens = [[i for i in tokens if i not in en_stop]]
# print(stopped_tokens[:10])
# print("STOP!\n")
# #texts = [p_stemmer.stem(i) for i in stopped_tokens]
#
# print("DIC!\n")
# # corpus = corpora.textcorpus.TextCorpus(dir)#[dictionary.doc2bow(text) for text in texts]
# # dictionary = corpora.textcorpus.TextDirectoryCorpus(dir)
# dictionary = corpora.Dictionary(stopped_tokens)
# print("CORPUS!\n")
# # convert tokenized documents into a document-term matrix
# corpus = [dictionary.doc2bow(t) for t in stopped_tokens]
# #dictionary = corpora.Dictionary.load_from_text("text8")
# print("START!\n")
# ldamodel = ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=20)
# print(ldamodel.print_topics(num_topics=3, num_words=3))
# sentences = word2vec.Text8Corpus('text8')
# model = word2vec.Word2Vec(sentences, size=200)
model = word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
print(model.most_similar(positive=['spain', 'paris'],negative=['france'], topn=3))

# model.wv.save_word2vec_format('text8.model.bin', binary=True)

