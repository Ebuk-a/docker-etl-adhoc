import json
from urllib.request import urlopen
import pandas as pd
import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy import text

postgres_engine = create_engine('postgresql://postgres:postgres@postgres:5432/postgres', connect_args={'connect_timeout': 10}, echo=False)

def load_api_userdata(batch_size=100):
    """Accepts a batch_size (number of pages, between 0-100) to read, and returns the raw users data and the cleaned data)"""
    page = urlopen("https://random-data-api.com/api/v2/users?size={}".format(batch_size))                         
    users_data = json.loads(page.read())
    users_raw= pd.json_normalize(users_data)

    return(users_raw)


def transform_user_df(raw_df:pd.DataFrame = load_api_userdata()) -> pd.DataFrame:
    users_prod= raw_df[['first_name', 'last_name','gender', 'address.country']]
    users_prod.rename(columns={'address.country': 'country'}, inplace=True)
    return (raw_df,users_prod)


def test_engine_connection(engine):
    """Tests Connection to PostgresDB"""
    try:
        with engine.connect() as con:
            con.execute(text("SELECT 1"))
        print('engine is valid and running')
    except Exception as e:
        print(f'Engine invalid: {str(e)}')


def write_to_db(
    df: pd.DataFrame,
    table_name: str,
    schema: str,
    engine: str = postgres_engine,
    dtype: dict = None,
    index: bool = False):

    df.to_sql(table_name, engine, schema=schema, if_exists='append', method='multi', chunksize= 500)


def run_etl() -> pd.DataFrame:
    """Main program that executes the ETL"""
    print('Fetching api data from "https://random-data-api.com/api/v2/users"')
    users_raw, users_prod= transform_user_df()
    
    print ("\nPrinting a sample of user's data fetched\n" + str(users_prod.head))

    print("\nTesting database connection...\n")
    test_engine_connection(postgres_engine)
    
    print("\nWriting raw data to staging.users_raw and transformed data to analytics.users\n")
    write_to_db(users_raw, table_name='users_raw', schema='staging', dtype={"id": sqlalchemy.types.VARCHAR(30)})
    write_to_db(users_prod, table_name='users', schema='analytics')
    print("Sucessfully updated tables staging.users_raw and analytics.users")

    return(users_prod.head)


if __name__== "__main__":
    run_etl()