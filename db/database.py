# import databases
# import sqlalchemy


# # SQLAlchemy specific code, as with any other app
# DATABASE_URL = "sqlite:///mockup_azure_sql.db"
# # DATABASE_URL = "postgresql://user:password@postgresserver/db"

# database = databases.Database(DATABASE_URL)

# metadata = sqlalchemy.MetaData()

# notes = sqlalchemy.Table(
#     "notes",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("text", sqlalchemy.String),
#     sqlalchemy.Column("completed", sqlalchemy.Boolean),
# )


# engine = sqlalchemy.create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )
# metadata.create_all(engine)

fake_users_db = {
    "tester": {
        "username": "tester",
        "email": "tester@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
    },
    "josh": {
        "username": "josh",
        "email": "josh@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
    }
}
