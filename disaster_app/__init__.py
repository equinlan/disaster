import pandas as pd
import json, pickle, plotly, sqlite3
import plotly.express as px

from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine

app = Flask(__name__)

# Load model
clf = pickle.load(open('models/classifier.pkl', 'rb'))

# Load data
engine = create_engine('sqlite:///data/DisasterResponse.db')
with engine.connect() as connection:
    df = pd.read_sql("SELECT * FROM messages", connection)

# Define classes
classes = [
    'Related',
    'Request',
    'Offer',
    'Aid Related',
    'Medical Help',
    'Medical Products',
    'Search and Rescue',
    'Security',
    'Military',
    'Child Alone',
    'Water',
    'Food',
    'Shelter',
    'Clothing',
    'Money',
    'Missing People',
    'Refugees',
    'Death',
    'Other Aid',
    'Infrastructure Related',
    'Transport',
    'Buildings',
    'Electricity',
    'Tools',
    'Hospitals',
    'Shops',
    'Aid Centers',
    'Other Infrastructure',
    'Weather Related',
    'Floods',
    'Storm',
    'Fire',
    'Earthquake',
    'Cold',
    'Other Weather',
    'Direct Report']

@app.route('/')
def index():
    # Make first figure
    df_melted = df.drop(columns=['message', 'genre']).melt()
    df_hist1 = df_melted[df_melted['value'] == True]
    fig1 = json.dumps(px.histogram(df_hist1, x="variable"), cls=plotly.utils.PlotlyJSONEncoder)

    # Make second figure
    df_lengths = df['message'].apply(lambda message: len(message)).rename('message_length')
    df_hist2 = df_lengths[df_lengths <= 500]
    fig2 = json.dumps(px.histogram(df_hist2, x='message_length'), cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', fig1=fig1, fig2=fig2, classes=classes)
@app.route('/_predict')
def predict():
    message = request.args.get('message')
    predictions = clf.predict([message]).tolist()
    return jsonify(predictions[0])