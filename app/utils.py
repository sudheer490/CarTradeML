import configparser
import psycopg2
import psycopg2.extras
import pandas as pd

def carviews():
    '''
    Get a list of car views.

    Returns:
    list: A list of car views as dictionaries with 'key' and 'value'.
    '''
    return [
        {
            'key': 'pickups',
            'value': 'Pickup',
            'invertText': True,
        },
        {
            'key': 'suv',
            'value': 'SUV',
            'invertText': True,
        },
        {
            'key': 'hatchback',
            'value': 'Hatchback',
            'invertText': True,
        },
        {
            'key': 'coupe',
            'value': 'Coupe',
            'invertText': False,
        },
        {
            'key': 'sedan',
            'value': 'Sedan',
            'invertText': False,
        },
        {
            'key': 'convertible',
            'value': 'Convertible',
            'invertText': False,
        },
        {
            'key': 'minivan',
            'value': 'Minivan',
            'invertText': True,
        },
        {
            'key': 'wagon',
            'value': 'Wagon',
            'invertText': False,
        },
    ]

def get_sql_conn(sql_conf: configparser.SectionProxy, dbname: str = None):
    '''
    Get a SQL database connection.

    Parameters:
    sql_conf (configparser.SectionProxy): Configuration settings for the database.
    dbname (str): Name of the database (default to None).

    Returns:
    psycopg2.extensions.connection: A database connection object.
    '''
    if dbname is None:
        dbname = sql_conf.get('dbname')
    production_db = psycopg2.connect(host=sql_conf['host'],
                                    database=sql_conf['dbname'],
                                    user=sql_conf['user'],
                                    password=sql_conf['password'])
    return production_db

def get_confg(path: str):
    '''
    Get configuration settings from a file.

    Parameters:
    path (str): Path to the configuration file.

    Returns:
    configparser.ConfigParser: A configuration parser object.
    '''
    config = configparser.ConfigParser()
    _ = config.read(path)
    return config
