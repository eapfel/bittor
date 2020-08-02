from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB_FILE = 'sqlite:///' + os.path.dirname(os.path.abspath('../../')) + '/data/bittor.db'

# DB_FILE = Config().get('database').get('url')

engine = create_engine('postgresql://bittor:Vcqvpa01@localhost:5432/bittor')  # (DB_FILE)  #
Session = sessionmaker(bind=engine)

Base = declarative_base()
