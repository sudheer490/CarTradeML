import pandas as pd
import numpy as np
import random

from flask import Flask, jsonify, render_template, request

from utils import get_confg, get_sql_conn, carviews
from searches import Search
from model.predict import make_prediction

import warnings

# Suppress all warnings for cleaner output
warnings.filterwarnings("ignore")

# Initialize Flask app
app = Flask(__name__)

# Configuration setup
config_path = '../app/schema/app.conf'
config = get_confg(config_path)

# Initialize search object for operations
search = Search(config=config)
carTypesView = carviews()

@app.route("/",methods=['GET', 'POST'])
def home():
    '''
    Home endpoint showing the main search page.
    '''
    allCars = search.getAllCars()
    return render_template('index.html', allCars=allCars, carTypes=carTypesView)

@app.route("/results",methods=['POST'])
def results():
    '''
    Endpoint that handles the search functionality and displays results.
    '''
    if request.method == 'POST':
        searchTerm = request.form.get('search-term')
        searchType = request.form.get('type')

        # Process and display results based on search type
        searchResult = search.getSearchResult(searchTerm=searchTerm,searchType=searchType)
        searchResult = search.processSearch(searchResult=searchResult,searchTerm=searchTerm)
        allCars = search.getAllCars()
        return render_template('results.html', searchTerm=searchTerm, results=searchResult, allCars=allCars)

@app.route('/results-view', methods=['POST'])
def results_view():
    '''
    Endpoint that displays a detailed view of a specific car.
    '''
    if request.method == 'POST':
        product_id = request.form.get('productId')
        car = search.getProduct(product_id)
        car = search.processResultsView(car)
        print("✅ Debugging: Car Details Path -", car.get("path"))  # Debugging

        
        conn = get_sql_conn(config['sql-prod'], config.get('sql-prod', 'bi_db'))
        features_car = pd.read_sql('''select * from car_features where cf_car_id ={} '''.format(int(product_id)),conn)
        similarSearches = pd.read_sql('''select * from similarity_matrix where cd_id = {id_} '''.format(id_=float(product_id)), conn)
        conn.close()
        features_car = features_car.drop(['cf_car_id'],axis=1)
        features_car.columns = [i.replace('cf_','') for i in features_car.columns]
        features_car = features_car.T.to_dict()[0]
        similarSearches = similarSearches.drop(['cd_id'],axis=1)
        similarSearches = [int(val) for val in similarSearches.values[0]]
        similarSearches = random.sample(similarSearches,3)
        conn = get_sql_conn(config['sql-prod'], config.get('sql-prod', 'bi_db'))
        similarCars = pd.read_sql('''select cd_id as id, cd_year as year, cd_make as make,cd_model as model,cd_car_price as price,cd_path_ as path from car_details where cd_id in {ids} '''.format(ids=tuple(similarSearches)), conn)
        conn.close()
        similarCars['path'] = similarCars.path.apply(lambda car: car.split('.')[0] + '.webp')
        similarCars = similarCars.T.to_dict()
        similarCars = [similarCars[i] for i in similarCars.keys()]
        return render_template('results-view.html', carDetails=car,similarCars=similarCars, featuresCar=features_car)

import logging
import os

# Ensure the log file is created
log_file = "sell_logs.log"
if not os.path.exists(log_file):
    open(log_file, 'w').close()  # Create the file if it does not exist

# Configure logging with file handler
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

logging.info("Logging initialized successfully.")
 
@app.route('/sell', methods=['GET', 'POST'])
def sell():    
    '''
    Endpoint that handles the functionality of selling a car.
    '''
    logging.info("Sell endpoint accessed. Method: %s", request.method)

    try:
        # Get possible searches from the database
        conn = get_sql_conn(config['sql-prod'], config.get('sql-prod', 'bi_db'))
        possibleSearches = pd.read_sql(
            '''SELECT cd_body_style, cd_make as car_make, cd_model FROM car_details''', conn)
        conn.close()

        possibleSearches = possibleSearches[possibleSearches.cd_body_style != 'NaN']
        possibleSearchesCarType = possibleSearches.groupby(['cd_body_style']).agg(
            Makes=('car_make', lambda x: list(set(x)))).to_dict()
        carTypes = list(possibleSearchesCarType.get('Makes').keys())

        conn = get_sql_conn(config['sql-prod'], config.get('sql-prod', 'bi_db'))
        doors = pd.read_sql('''SELECT DISTINCT cd_doors AS doors FROM car_details WHERE cd_doors != 'NaN' ''', conn).to_dict()
        transmission = pd.read_sql('''SELECT DISTINCT cd_transmission AS transmission FROM car_details WHERE cd_transmission != 'NaN' ''', conn).to_dict()
        engine = pd.read_sql('''SELECT DISTINCT cd_engine AS engine FROM car_details WHERE cd_engine != 'NaN' ''', conn).to_dict()
        driveType = pd.read_sql('''SELECT DISTINCT cd_drive_type AS drive_type FROM car_details WHERE cd_drive_type != 'NaN' ''', conn).to_dict()
        fuel = pd.read_sql('''SELECT DISTINCT cd_fuel AS fuel FROM car_details WHERE cd_fuel!='NaN' ''', conn).to_dict()
        conn.close()

        doors = list(doors['doors'].values())
        doors = [int(i.split(' ')[0]) for i in doors]
        transmission = list(transmission['transmission'].values())
        engine = list(engine['engine'].values())
        driveType = list(driveType['drive_type'].values())
        fuel = list(fuel['fuel'].values())

        # Handle POST actions for selling a car
        if request.method == 'POST':
            action = request.form.get('action')
            logging.info("Received POST request with action: %s", action)

            if action == 'getCarMake':
                car_type = request.form.get('carType')
                logging.info("Fetching car makes for car type: %s", car_type)
                result_car_make = list(possibleSearchesCarType.get('Makes').get(car_type))
                return jsonify(result_car_make)

            if action == 'getCarModel':
                carMake = request.form.get('carMake')
                car_type = request.form.get('carType')
                logging.info("Fetching car models for make: %s and type: %s", carMake, car_type)
                possibleSearchesCarModel = possibleSearches[
                    (possibleSearches.car_make == carMake) & (possibleSearches.cd_body_style == car_type)
                ].groupby(['car_make']).agg(Models=('cd_model', lambda x: list(set(x)))).to_dict()
                carTypes = list(possibleSearchesCarModel.get('Models').values())[0]
                return jsonify(carTypes)

            if action == 'getCarPrice':
                features = pd.DataFrame()
                f = request.form

                for key in f.keys():
                    for value in f.getlist(key):
                        features[key] = [value]

                features = features.rename(columns={'mileage_miles': 'miles_driven', 'door': 'doors'})
                features['avg_mpg'] = 0.5 * (features['city_mpg'].astype(float) + features['hwy_mpg'].astype(float))

                logging.info("Features extracted before prediction: %s", features.to_dict(orient='records'))

                predictedPrice = make_prediction(features=features)
                logging.info("Predicted price: %s", predictedPrice)

                return jsonify({'price': predictedPrice})

    except Exception as e:
        logging.error("Error in /sell endpoint: %s", str(e), exc_info=True)
        return jsonify({'error': 'An error occurred, please try again later.'}), 500

    return render_template('sell.html', carTypes=carTypes, doorList=doors, transmissionList=transmission,
                           engineList=engine, driveTypeList=driveType, fuelTypeList=fuel)

# Entry point for the Flask app
if __name__ == "__main__":
    app.run(debug=True)
