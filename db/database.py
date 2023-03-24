# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
# from sqlalchemy.orm import sessionmaker

# # Define database information
# engine = create_engine('sqlite:///mockup_azure_sql.db')
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# metadata = MetaData()

# # Define the table structure
# users = Table('users', metadata,
#               Column('id', Integer, primary_key=True),
#               Column('username', String),
#               Column('email', String),
#               Column('password', String))
