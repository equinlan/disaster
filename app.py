import nltk, re

from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.corpus.reader.wordnet import ADJ, ADV, NOUN, VERB
from nltk.stem import WordNetLemmatizer

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def convert_pos_tag(tag):
    # https://www.programcreek.com/python/example/91610/nltk.corpus.wordnet.NOUN
    if tag in ['JJ', 'JJR', 'JJS']:
        return ADJ
    elif tag in ['RB', 'RBR', 'RBS']:
        return ADV
    elif tag in ['NN', 'NNS', 'NNP', 'NNPS']:
        return NOUN
    elif tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return VERB
    return NOUN

def tokenize(text):
    tokens = word_tokenize(text)
    words = [token for token in tokens if re.match("[a-zA-Z0-9]", token)]
    no_stopwords = [word for word in words if word not in stopwords.words("english")]
    lowercase_words = [word.lower() for word in no_stopwords]
    pos_tagged_words = pos_tag(lowercase_words)
    lemmatized_words = [WordNetLemmatizer().lemmatize(word, pos=convert_pos_tag(pos)) for word, pos in pos_tagged_words]
    return lemmatized_words

from app import app

app.run(host='localhost', port=3001, debug=True)