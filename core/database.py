import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Sentence(Base):
    __tablename__ = "sentences"
    id = Column(Integer, primary_key=True)
    parent_text = Column(String)
    child_text = Column(String)

    def __repr__(self):
        return "<Sentence(parent_text='%s', child_text='%s')>" % (
            self.parent_text,
            self.child_text,
        )


class DataBase:
    def __init__(self, database_path):
        self.engine = sqlalchemy.create_engine(f"sqlite:///{database_path}")
        self.verify_integrity()

        SessionClass = sessionmaker()
        SessionClass.configure(bind=self.engine)
        self.session = SessionClass()

    def verify_integrity(self):
        if not self.engine.dialect.has_table(self.engine, "sentences"):
            Base.metadata.create_all(self.engine)

    def clear_database(self):
        self.session.query(Sentence).delete()

    def add_sentence_list(self, sentence_list):
        row_list = []

        for sentence in sentence_list:
            row_list.append(Sentence(parent_text=sentence[0], child_text=sentence[1]))

        self.session.add_all(row_list)
        self.session.commit()

    def add_sentence(self, **kwargs):
        sentence = Sentence(
            parent_text=kwargs["parent_text"], child_text=kwargs["child_text"]
        )
        self.session.add(sentence)
        self.session.commit()

    def get_sentence_list(self):
        return self.session.query(Sentence, Sentence.parent_text).all()
