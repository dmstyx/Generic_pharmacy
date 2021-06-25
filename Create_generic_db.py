from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import time
import India_mart_scraper

Base = declarative_base()
engine = create_engine('sqlite:///Generic_names.db?check_same_thread=False')


class Table(Base):
    __tablename__ = 'Drugs'
    id = Column(Integer, primary_key=True)
    brand_name = Column(String, default='No Brand Name')
    generic_name = Column(String, default='No Generic Name')

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_names_to_db():
    a = []
    b = []
    with open('generic_drugs.txt', 'r') as f:
        for count, line in enumerate(f, start=1):
            if count % 2 == 0:
                a.append(line.strip())
            else:
                b.append(line.strip())
    x = tuple(zip(a, b))

    for i in x:
        new_row = Table(generic_name=i[0], brand_name=i[1])
        session.add(new_row)
        session.commit()


def get_names_from_db():
    get_data = session.query(Table).all()
    for data in get_data:
        print(f'The ID is: {data.id}, Brand name: {data.brand_name} Generic name is: {data.generic_name}')
        India_mart_scraper.format_text(data.generic_name, data.brand_name)
        time.sleep(2)


session.close()

if __name__ == "__main__":
    get_names_from_db()

