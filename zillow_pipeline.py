import sqlite3
import sqlite_db as sdb
import zillow_scrape
import zillow_webdriver
import pandas as pd
import time

def get_address_from_sqlite(conn):

    df = pd.read_sql('SELECT * FROM open_street_maps_residential LIMIT 10', conn)

    return df

if __name__ == '__main__':

    #check if address exists in zillow_housing_attributes table (reduce API calls)
    #scrape zillow for the address
    #insert or update into zillow_housing_attributes
    conn = sqlite3.connect('housing_pipeline_ml.db')
    df = get_address_from_sqlite(conn)


    for i in df.iterrows():

        check_table = pd.read_sql(f"SELECT * FROM zillow_house_attributes WHERE streetAddress = '{i[1]['streetAddress']}'", conn)

        if len(check_table) == 0:

            address = f"{i[1]['streetAddress']} {i[1]['city']}, {i[1]['state']} {i[1]['zipcode']}"
            # df = zillow_scrape.get_house_attributes(address)
            df = zillow_webdriver.get_house_attributes(address)

            if df is not None:
                sdb.insert_without_duplicates(df, conn, "zillow_house_attributes")

            time.sleep(5)

        else:
            print("Record already exists for this property")
            pass


    conn.close()
    pass
