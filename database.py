# import urllib
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

cnxn_string = 'sqlite:///mockup_azure_sql.db'


# server = ''
# database = ''
# username = ''
# password = ''
# driver = 'ODBC Driver 17 for SQL Server'

# driver = '{ODBC Driver 17 for SQL Server}'

# odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID=' + \
#     ';PORT=1433;UID='+username+';DATABASE=' + database + ';PWD=' + password

# cnxn_string = f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver={driver}"
# cnxn_string = 'mssql+pyodbc:///?odbc_connect=' + urllib.quote_plus(odbc_str)\

engine = create_engine(cnxn_string)
SessionLocal = sessionmaker(bind=engine)

# Create metadata
metadata = MetaData()

# Connect to the engine
conn = engine.connect()

# Create a new database file named "mockup_azure_sql.db"
conn.execute("CREATE DATABASE mockup_azure_sql")  # SQLite specific syntax


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
