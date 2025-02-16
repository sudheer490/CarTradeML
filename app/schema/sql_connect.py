import configparser
import psycopg2
import psycopg2.extras
import pandas as pd

class Connections:
    def __init__(self,conf_path:str):
        self.conf_path = conf_path
    
    def get_confg(self):
        config = configparser.ConfigParser()
        _ = config.read(self.conf_path)
        return config
    
    def get_sql_conn(self,sqlConfPath:configparser.SectionProxy,dbname: str = None):
        if dbname is None:
            dbname = sqlConfPath.get('dbname')
        prodution_db = psycopg2. \
            connect(host=sqlConfPath['host'],
                    database=sqlConfPath['dbname'],
                    user=sqlConfPath['user'],
                    password=sqlConfPath['password'])
        return prodution_db
    def push_to_sql(self,data: pd.DataFrame, config: configparser.ConfigParser,table:str,primary_key:str):
        table = config['sql-table'][table]
        pk = config['sql-table'][primary_key]
        df_columns = list(data)
        columns = ",".join(df_columns)
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))
        updates = ','.join([col + '=excluded.' + col for col in df_columns])
        insert_stmt = "INSERT INTO {} ({}) {} ON CONFLICT ({}) DO UPDATE SET {}". \
            format(table, columns, values, pk, updates)
        conn = self.get_sql_conn(config['sql-prod'],
                            config.get('sql-prod', 'bi_db'))
        cur = conn.cursor()
        psycopg2.extras.execute_batch(cur, insert_stmt, data.values)
        conn.commit()
        cur.close()
        conn.close()