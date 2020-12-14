"""The models module."""

from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper

metadata = MetaData()
groups_table = Table(
    'group', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
)
students_table = Table(
    'student', metadata,
    Column('id', Integer, primary_key=True),
    Column('group_id', String),
    Column('first_name', String),
    Column('last_name', String),
)
courses_table = Table(
    'course', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
)



class GroupModel(object):
    def __init__(self, name):
        self.name = name


class StudentModel(object):
    def __init__(self, group_id, first_name, last_name):
        self.group_id = group_id
        self.first_name = first_name
        self.last_name = last_name


class CourseMode(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
