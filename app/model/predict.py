import pickle
import pandas as pd
import numpy as np
#load the stacking model

file_path = './model/stacking_pipeline.pkl'


try:
    # Open and load the pickle file
    with open(file_path, 'rb') as file:
        loaded_data = pickle.load(file)
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

import logging
import numpy as np
import pandas as pd
 
# Ensure logging is set up properly
log_file = "sell_logs.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def make_prediction(features: pd.DataFrame):
    '''
    Predict car price given feature set.
    '''
    try:
        logging.info("Received features for prediction: %s", features.to_dict(orient='records'))

        bin_features = ['apple_carplay', 'backup_camera_assist', 'bluetooth', 'heated_seats',
                        'hill_assist_system', 'keyless_entry', 'keyless_ignition', 'multimedia_telematics',
                        'premium_sound_system', 'satellite_radio', 'sunroof_moonroof', 'leather_seats', 'power_seats',
                        'traction_control', 'driver_assistance_confidence_pkg', 'head-up_display',
                        'lane_departure_warning', 'navigation_system', 'remote_start', 'blind_spot_monitor',
                        'lane_assist', 'parking_assist_system', 'stability_control', 'adaptive_cruise_control',
                        'alloy_wheels', 'cooled_seats', 'full_self-driving_capability', 'third_row_seating',
                        'tow_hitch_package', 'rear_seat_entertainment']

        cols = ['type', 'make', 'year', 'model', 'miles_driven', 'doors', 'engine',
                'transmission', 'drive_type', 'fuel'] + bin_features + ['avg_mpg']

        # Select only required columns
        features = features[cols]

        # Ensure 'type' is lowercase
        features['type'] = features['type'].str.lower()

        # Convert data types
        features['year'] = features['year'].astype(int)
        features['miles_driven'] = features['miles_driven'].astype(float)

        # Fill missing binary feature values with 0 and convert to integers
        features[bin_features] = features[bin_features].fillna(0).astype(int)

        # Create 'bin_sum' column (sum of binary features) and ensure it's numeric
        features['bin_sum'] = features[bin_features].sum(axis=1).astype(int)

        # Categorize cars into 'lux_category' based on 'bin_sum'
        features['lux_category'] = features['bin_sum'].apply(lambda x: 1 if x >= 11 else 0)
        logging.info(features)
        logging.info(features.shape)
        features = features[['type', 'make', 'year', 'model', 'miles_driven', 'doors', 'engine',
       'transmission', 'drive_type', 'fuel', 'avg_mpg', 'lux_category']]
        logging.info(features)
        logging.info(features.shape)
        logging.info("Processed feature values before prediction: %s", features.to_dict(orient='records'))
        logging.info("Feature data types: %s", features.dtypes.to_dict())
        logging.info("Luxury category distribution: %s", features['lux_category'].value_counts().to_dict())
        features = features.applymap(lambda x: x.lower() if isinstance(x, str) else x)
        logging.info(features.dtypes)
        # Convert data types explicitly
        features = features.astype({
            "type": "object",
            "make": "object",
            "year": "float64",   # Change from int64 to float64
            "model": "object",
            "miles_driven": "float64",
            "doors": "object",   # Change from int64 to object (string)
            "engine": "object",
            "transmission": "object",
            "drive_type": "object",
            "fuel": "object",
            "avg_mpg": "float64",
            "lux_category": "int64"
        })

        # Print DataFrame to check changes
        logging.info(features.dtypes)
        logging.info(features)
        prediction = loaded_data.predict(features)
        predicted_price = np.round(prediction[0], 3)

        logging.info("Predicted price: %s", predicted_price)
        return predicted_price
    except Exception as e:
        logging.error("Error in make_prediction function: %s", str(e), exc_info=True)
        return None  # Handle errors gracefully
        