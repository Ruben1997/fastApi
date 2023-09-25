from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'mysql+pymysql://ecotourlaplata_ecotourlaplata:TpAc?5130@162.214.120.119:3306/ecotourlaplata_blogapplication'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()