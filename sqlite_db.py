from sqlalchemy import create_engine, Column, Integer, DateTime, Float, String, update
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
import os

def init_db():

    #Define db
    engine = create_engine('sqlite:///housing_pipeline_ml.db')

    base = declarative_base()

    class OpenStreetMapsResidential(base):
        __tablename__ = 'open_street_maps_residential'
        id = Column(Integer, primary_key=True, autoincrement=True)
        city = Column(String)
        houseNumber = Column(Integer)
        zipcode = Column(Integer)
        state = Column(String)
        street = Column(String)
        streetAddress = Column(String)
        source = Column(String)

    class ZillowHouseAttributes(base):
        __tablename__ = 'zillow_house_attributes'
        id = Column(Integer, primary_key=True, autoincrement=True)
        streetAddress = Column(String)
        city = Column(String)
        state = Column(String)
        zipcode = Column(Integer)
        longitude = Column(Float)
        latitude = Column(Float)
        homeType = Column(String)
        yearBuilt = Column(Integer)
        livingArea = Column(Integer)
        lotSize = Column(Integer)
        hoaFee = Column(Float)
        bathroomsFloat = Column(Float)
        bedrooms = Column(Integer)
        parkingCapacity = Column(Integer)
        hasHeating = Column(String)
        hasPrivatePool =Column(String)

    # class ZillowPricing(base):
    #     __tablename__ = 'reddit_transform'
    #     id = Column(Integer, primary_key=True, autoincrement=True)


    base.metadata.create_all(engine)

def delete_db(db_path):

    # Create an engine connected to the SQLite database
    engine = create_engine(f'sqlite:///{db_path}')

    # Dispose of the engine to close all connections
    engine.dispose()

    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Database '{db_path}' deleted successfully.")
    else:
        print(f"Database '{db_path}' does not exist.")


def insert_without_duplicates(df, conn, table_name, insertion_mode='IGNORE'):
    """
    to insert or ignore i need 2 things:
        - formatted string of column names
            - (column1, column2, column3, ... )
        - formatted string of row placeholders
            - (?, ?, ?, ... )

    the cursor.execute(sql, tuple) will replace the placeholders with the values from the tuple
        - cursor.execute() will cause the insertion to go row by row and i will need to iterate

    I can do a bulk insertion using cursor.executemany(sql, data)
        - where data are the value rows from my dataframe
    """

    cursor = conn.cursor()

    columns = df.columns.tolist()
    placeholders = ', '.join(['?'] * len(columns))

    #f-string to SQL format
    sql = f"INSERT OR {insertion_mode} INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    #bulk data insertion
    data = df.values.tolist()
    cursor.executemany(sql, data)

    conn.commit()
    cursor.close()


if __name__ == '__main__':


    # delete_db('reddit_smp_sentiment.db')
    init_db()