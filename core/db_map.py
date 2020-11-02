from contextlib import contextmanager

import redis
from sqlalchemy import Column, BigInteger, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import config

Base = declarative_base()
engine = create_engine(config.DATABASE_URL, echo=False, pool_size=8, max_overflow=12)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

r = redis.from_url(
    'redis://h:p10e8b82a51565c3ecd69eab427fc7fa7942d61bbbc81d56cabdde0f49bc02c18@ec2-52-1-57-198.compute-1.amazonaws.com:25729')


@contextmanager
def session_scope():
    session = Session()

    try:
        yield session
        session.commit()

    except:
        session.rollback()
        raise

    finally:
        session.close()


class UsersTable(Base):
    __tablename__ = 'users_table'
    id = Column(BigInteger, primary_key=True, nullable=False)
    side = Column(BigInteger, default=0, nullable=False)
