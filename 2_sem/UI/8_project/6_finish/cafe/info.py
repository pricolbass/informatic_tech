from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import or_


Base = declarative_base()

RUSSIAN_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
START_TIME = (10, 0)
END_TIME = (21, 0)
MAX_TABLES = {
    "Обычный": 15,
    "VIP": 5,
    "На террасе": 10
}
DELTA_HOUR = 1


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, default='client')


class MenuItem(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    photo_path = Column(String)
    price = Column(Integer, nullable=False)
    type = Column(String, nullable=False)

    def __repr__(self):
        return f"<MenuItem(type='{self.type}', name='{self.name}', description='{self.description}', price={self.price})>"


class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    guest_count = Column(Integer, nullable=False)
    table_type = Column(String, nullable=False)
    special_requests = Column(String)
    first_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    def __repr__(self):
        return f"<Reservation(date='{self.date}', time='{self.time}', guest_count={self.guest_count}, table_type='{self.table_type}', special_requests='{self.special_requests}')>"


class Journal(Base):
    __tablename__ = 'journal'
    id = Column(Integer, primary_key=True)
    action = Column(String, nullable=False)
    time = Column(String, nullable=False)
    details = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    def __repr__(self):
        return f"<JournalEvent(action='{self.action}', time='{self.time}', details='{self.details}', first_name='{self.first_name}', last_name='{self.last_name}', role='{self.role}')>"


engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

inspector = inspect(engine)
column_names_users = [column['name'] for column in inspector.get_columns('users')]
column_names_journal = [column['name'] for column in inspector.get_columns('journal')]
column_names_menu = [column['name'] for column in inspector.get_columns('menu')]
column_names_reservation = [column['name'] for column in inspector.get_columns('reservations')]
