# Message Classification for Disaster Response

This code, generated as part of a Udacity course, provides the scaffold required to extract and classify disaster data from [Figure Eight|https://www.figure-eight.com/]. The data comes in the form of messages collected from social media during disasters, such as:

> We are more than 50 people sleeping on the street. Please help us find tent, food.

After training a machine learning classifier on the data, a message like the one above can be predicted on categories such as:

> Related, Request, Aid Related, Food, Shelter, Direct Report

These kinds of categorizations can help send messages to the appropriate aid and response organizations during disasters, which is exactly when there's no time to sift through such messages by hand.

# Using this repository

## Data

The code expects you have data in CSV format and in two files. The first file contains messages:

```
id,message,original,genre
2,Weather update - a cold front from Cuba that could pass over Haiti,Un front froid se retrouve sur Cuba ce matin. Il pourrait traverser Haiti demain. Des averses de pluie isolee sont encore prevues sur notre region ce soi,direct
7,Is the Hurricane over or is it not over,Cyclone nan fini osinon li pa fini,direct
8,Looking for someone but no name,"Patnm, di Maryani relem pou li banm nouvel li ak timoun yo. Mesi se john jean depi Monben kwochi.",direct
```

...and the second file contains message classifications:

```
id,categories
2,related-1;request-0;offer-0;aid_related-0;medical_help-0;medical_products-0;search_and_rescue-0;security-0;military-0;child_alone-0;water-0;food-0;shelter-0;clothing-0;money-0;missing_people-0;refugees-0;death-0;other_aid-0;infrastructure_related-0;transport-0;buildings-0;electricity-0;tools-0;hospitals-0;shops-0;aid_centers-0;other_infrastructure-0;weather_related-0;floods-0;storm-0;fire-0;earthquake-0;cold-0;other_weather-0;direct_report-0
7,related-1;request-0;offer-0;aid_related-1;medical_help-0;medical_products-0;search_and_rescue-0;security-0;military-0;child_alone-0;water-0;food-0;shelter-0;clothing-0;money-0;missing_people-0;refugees-0;death-0;other_aid-1;infrastructure_related-0;transport-0;buildings-0;electricity-0;tools-0;hospitals-0;shops-0;aid_centers-0;other_infrastructure-0;weather_related-1;floods-0;storm-1;fire-0;earthquake-0;cold-0;other_weather-0;direct_report-0
8,related-1;request-0;offer-0;aid_related-0;medical_help-0;medical_products-0;search_and_rescue-0;security-0;military-0;child_alone-0;water-0;food-0;shelter-0;clothing-0;money-0;missing_people-0;refugees-0;death-0;other_aid-0;infrastructure_related-0;transport-0;buildings-0;electricity-0;tools-0;hospitals-0;shops-0;aid_centers-0;other_infrastructure-0;weather_related-0;floods-0;storm-0;fire-0;earthquake-0;cold-0;other_weather-0;direct_report-0
```

## Pipelines

This repository contains an ETL pipeline, `data/process_data.py`, that extracts the CSV data and saves it to an SQLite database. To run the ETL pipeline, give it three arguments:

1. The messages CSV
2. The categories CSV
3. The path for the new SQLite database

For example:

`python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`

This repository also contains an ML pipeline, `models/train_classifier.py`, that trains, pickles, and saves a classifier based on the SQLite database data. To run the ML pipeline, give it two arguments:

1. The SQLite database
2. The pickled classifier

For example:

`python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

## Web Application

This repository contains a web application written in Flask that displays some visualizations of the training data and allows testing of the message classifier:

`python app.py`

:warning: The web application will expect `classifier.pkl` in the `models` directory, and unfortunately it is too large to upload to GitHub. Please download a ZIP containing the file here:

https://drive.google.com/file/d/1II186SABUqAluIfhbogrA-8SaPb6xTr0/view?usp=sharing

Once you have downloaded it, extract `classifier.pkl` to the `models` directory.

## Dependencies

- Python 3.7
- Pandas
- SQLAlchemy
- NLTK
- Scikit Learn
- Flask
