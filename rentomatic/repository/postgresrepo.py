from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rentomatic.repository.postgres_objects import Base, Room
from rentomatic.domain import room


class PostgresRepo:
    def __init__(self, connection_data):
        connection_string = "postgresql+psycopg2://{}:{}@{}/{}".format(
            connection_data['user'],
            connection_data['password'],
            connection_data['host'],
            connection_data['dbname']
        )

        self.engine = create_engine(connection_string)
        Base.metadata.bind = self.engine

    def list(self, filters=None):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        query = session.query(Room)

        if filters is None:
            return query.all()

        if 'code__eq' in filters:
            query = query.filter(Room.code == filters['code__eq'])

        if 'price__eq' in filters:
            query = query.filter(Room.price == filters['price__eq'])

        if 'price__lt' in filters:
            query = query.filter(Room.price < filters['price__lt'])

        if 'price__gt' in filters:
            query = query.filter(Room.price > filters['price__gt'])

        return [
            room.Room(
                code=q.code,
                size=q.size,
                price=q.price,
                latitude=q.latitude,
                longitude=q.longitude
            )
            for q in query.all()
        ]
