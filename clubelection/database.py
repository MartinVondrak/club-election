from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, mapper, relationship

from clubelection.models import Voter, Candidate, Vote

metadata = MetaData()


def map_entities_to_tables():
    voter = Table('voter', metadata,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('access_code', String(36), nullable=False, unique=True),
                  Column('has_voted', Boolean, nullable=False, default=False)
                  )
    candidate = Table('candidate', metadata,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('first_name', String(255), nullable=False),
                      Column('last_name', String(255), nullable=False),
                      Column('biography', Text, nullable=False)
                      )
    vote = Table('vote', metadata,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('candidate_id', Integer, ForeignKey('candidate.id'), nullable=False)
                 )

    mapper(Voter, voter)
    mapper(Vote, vote, properties={
        'candidate': relationship(Candidate)
    })
    mapper(Candidate, candidate)


def init_database(db_connection_string: str, debug: bool):
    map_entities_to_tables()
    engine = create_engine(db_connection_string, echo=debug)
    metadata.create_all(engine)
    return sessionmaker(bind=engine)
