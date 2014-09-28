from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    number = Column(String(50), unique=True)

    def __init__(self, number=None):
        self.number = number

    def __repr__(self):
        return '<Session %r>' % (self.number)


class Expression(Base):
    __tablename__ = 'expressions'
    id = Column(Integer, primary_key=True)
    expr_str = Column(String(256), unique=False)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    session = relationship(
        Session,
        backref=backref('expressions',
                         uselist=True,
                         cascade='delete,all,delete-orphan'))

    def __init__(self, expr_str=None):
        self.expr_str = expr_str

    def __repr__(self):
        return '<Expression %r>' % (self.expr_str)
