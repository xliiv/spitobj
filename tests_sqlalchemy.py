import unittest

import spitobj

# there must be a better way
try:
    import sqlalchemy
    from sqlalchemy import Column, Integer, String, Sequence
    from sqlalchemy.orm import sessionmaker, scoped_session
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base


    Base = declarative_base()
    engine = create_engine('sqlite:///:memory:')
    session = scoped_session(sessionmaker(bind=engine))


    class PersonModel(Base):
        __tablename__ = 'people'
        id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
        nickname = Column(String(50))


    class PersonSqlalchemySpitter(spitobj.SpitobjSqlalchemy):
        obj_class = PersonModel
        sqlalchemy_session = session
        fields = (
            ('nickname', spitobj.StringGenerator()),
        )


    Base.metadata.create_all(engine)


    class TestSpitobjSqlalchemy(unittest.TestCase):

        def test_save_works(self):
            PersonSqlalchemySpitter.get_saved()

            obj = session.query(PersonModel).first()
            assert obj.nickname != ''
            assert isinstance(obj.id, int)


    if __name__ == '__main__':
        unittest.main()

except ImportError:
    print("Install sqlalchemy to test this module")
