"""The models module."""

from sqlalchemy import (Column, ForeignKey, Integer, String, Table,
                        create_engine)
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE = {
        'drivername': 'postgres',
        'host': 'localhost',
        'port': '5432',
        'username': 'Shavrin_Maksim',
        'password': '123456789',
        'database': 'students',
    }

Base = declarative_base()

engine = create_engine(URL(**DATABASE), echo=True)

Session = sessionmaker()

session = Session(bind=engine)

association_table = Table(
    'association',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('student.id')),
    Column('course_id', Integer, ForeignKey('course.id')),
)


class GroupModel(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return self.name


class StudentModel(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    group_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    courses = relationship(
        'CourseModel',
        secondary=association_table,
        backref="students",
        )

    def __init__(self, group_id, first_name, last_name):
        self.group_id = group_id
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        return f'\n{self.first_name} {self.last_name}: {self.group_id}'


class CourseModel(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        return self.name
