import nltk, pickle, re, sys
import pandas as pd

from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.corpus.reader.wordnet import ADJ, ADV, NOUN, VERB
from nltk.stem import WordNetLemmatizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sqlalchemy import create_engine

# Get command line arguments
db_path = sys.argv[1]
pickle_path = sys.argv[2]

# Download requisite nltk resources
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load data from database
engine = create_engine(f'sqlite:///{db_path}')
with engine.connect() as connection:
    df = pd.read_sql_table("messages", connection)

# Write a tokenization function to process text data
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

# Build a machine learning model
pipeline = Pipeline([
    ('vect', CountVectorizer(tokenizer=tokenize, ngram_range=(1, 2))),
    ('tfidf', TfidfTransformer()),
    ('clf', MultiOutputClassifier(RandomForestClassifier()))
])

# Train model with grid search
X = df['message']
y = df.drop(columns=['message', 'genre'])
X_train, X_test, y_train, y_test = train_test_split(X, y)

parameters = {
    "vect__ngram_range": [(1, 1), (1, 2)],
    "clf__estimator__n_estimators": [50, 100],
    "clf__estimator__max_features": ['sqrt', 'log2']}
cv = GridSearchCV(pipeline, parameters)
cv.fit(X_train, y_train)

# Print classification report
y_pred = cv.predict(X_test)
print(classification_report(y_test, y_pred, target_names=y_test.columns))

# Pickle model
s = pickle.dump(cv, open(pickle_path, "wb"))