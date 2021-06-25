from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Meds(Base):

    __tablename__ = 'medication'

    id = Column('id', Integer, primary_key=True)
    generic_name = Column('generic_name',String(100), default='Not Available')
    brand_name = Column('brand_name', String(100), default='Not Available')
    product_name = Column('product_name', String(200), default='Not Available')
    price = Column('price', Float, default='Not Available')
    packaging_size = Column('packaging_size', String(20), default='Not Available')
    Dose = Column('Dose', String(20), default='Not Available')
    Composition = Column('Composition', String(200), default='Not Available')
    Treatment = Column('Treatment', String(200), default='Not Available')
    Prescription = Column('Prescription', String(20), default='Not Available')
    Form = Column('Form', String(20), default='Not Available')
    Manufacturer = Column('Manufacturer', String(100), default='Not Available')
    company = Column('company', String(100), default='Not Available')
    contact = Column('contact', String(100), default='Not Available')
    address = Column('address', String(200), default='Not Available')
    Company_website = Column('Company_website', String(100), default='Not Available')
    telephone = Column('telephone', String(20), default='Not Available')
    image = Column('image', String(200), default='Not Available')
    im_website = Column('im_website', String(200), default='Not Available')


engine = create_engine('sqlite:///Meds_info.db?check_same_thread=False', echo=False)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()


def enter_med_info(data):

    meds = Meds()

    meds.generic_name = data[0]
    meds.brand_name = data[6]
    meds.product_name = data[1]
    meds.price = float(data[2])
    meds.packaging_size = (f'{data[11]} {data[12]}')
    meds.Dose = data[19]
    meds.Composition = (f'{data[15]} {data[16]}')
    meds.Treatment = (f'{data[17]} {data[18]}')
    meds.Prescription = (f'{data[19]} {data[20]}')
    meds.Form = (f'{data[21]} {data[22]}')
    meds.Manufacturer = (f'{data[13]} {data[14]}')
    meds.company = data[4]
    meds.contact = data[3]
    meds.address = data[5]
    meds.Company_website = data[8]
    meds.telephone = data[7]
    meds.image = data[10]
    meds.im_website = data[9]

    session.add(meds)
    session.commit()


def get_meds_info():
    get_by_id = session.query(Meds).all()

    for id in get_by_id:
        print(f'The ID is {id.id} & the Generic name is {id.generic_name}.')


def med_not_found():
    print('Generic Medication Not Found.')


session.close()
