import sys
import time
import pandas as pd 
import numpy as np
from sql_connect import Connections

def get_data(data_path):
    df = pd.read_excel(data_path)
    df = df[['make','model','year']]
    print(df.head())
    df['year'] = df.year.fillna(2023).astype(int)
    df = df.rename(columns={'model':'brand'})
    # df = df.drop_duplicates().reset_index(drop=True)
    df['id'] = df.index
    df.columns = ['car_' + i for i in df.columns]
    df = df[['car_id','car_make','car_brand','car_year']]
    return df

def get_data_car_details(data_path):
    df = pd.read_excel(data_path)
    df['year'] = df.year.fillna(2023).map(lambda x: int(x))
    path_ = pd.read_csv('../../data/paths.csv')
    df['make'] = df.make.map(lambda x: 'mercedes-benz' if x=='mercedes' else x)
    df['model'] = df.model.map(lambda x: str(x).replace('benz ','' ))
    df['make'] = df.make.map(lambda x: 'alfa-romeo' if x=='alfa' else x)
    df['model'] = df.model.map(lambda x: str(x).replace('romeo ','' ))

    df['search'] = df['make']+'_' + df.model.str.replace(' ','-').astype(str) + '_' + df.year.fillna(2023).astype(int).astype(str) 
    df = df.reset_index(drop=True)
    
    df = pd.merge(df,path_[['search','path_']],on='search')
    df['id'] = df.index
    df = df[['id','mileage_miles','price','year','make','model',
       'Body Style', 'Doors', 'MPG', 
       'Engine', 'Transmission', 'Drive Type', 'Fuel', 'Tank Size',
       'Bed Style', 'Cab Style','path_']]
    
    df = df.rename(columns={'price':'car_price'})
    df.columns = ['cd_'+i.lower().replace(' ','_')  for i in df.columns]
    return df

def get_similarity_matrix(data_path):
    df = pd.read_csv(data_path)
    df = df.drop(['Unnamed: 0'],axis=1)
    for col in df.columns:
        df[col] = df[col].apply(float)
    return df

def get_data_car_features(data_path):
    df = pd.read_excel(data_path)
    df['car_id'] = df.index
    
    df = df[['car_id','Android Auto', 'Apple CarPlay',
       'Backup Camera / Assist', 'Bluetooth', 'Heated Seats',
       'Hill Assist System', 'Keyless Entry', 'Keyless Ignition',
       'Multimedia / Telematics', 'Premium Sound System', 'Satellite Radio',
       'Sunroof / Moonroof', 'Leather Seats', 'Power Seats',
       'Traction Control', 'Driver Assistance / Confidence Pkg',
       'Head-Up Display', 'Lane Departure Warning', 'Navigation System',
       'Remote Start', 'Blind Spot Monitor', 'Lane Assist',
       'Parking Assist System', 'Stability Control', 'Adaptive Cruise Control',
       'Alloy Wheels', 'Cooled Seats', 'Full Self-Driving Capability',
       'Third Row Seating', 'Tow Hitch / Package', 'Rear Seat Entertainment']]
    df = df.fillna(0)
    df.columns = ['cf_'+i.lower().replace(' / ',' ').replace('-',' ').replace(' ','_')  for i in df.columns]
    return df

def main(conf_path: str,data_path:str):
    #main
    start_time = time.time()
    if conf_path is None:
        raise ValueError("Arguments missing: conf_path: str, date:str")

    conn = Connections(conf_path)

    config = conn.get_confg()

    data = get_similarity_matrix(data_path)
    conn.push_to_sql(data, config,table='table_similarity',primary_key = 'table_similarity_pk')
    time_taken   = time.time() - start_time
    print('Time taken = {} s'.format(round(time_taken,1)))

if __name__ == '__main__':
    main(*sys.argv[1:])