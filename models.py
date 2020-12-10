"""The models module."""

from sqlalchemy import Column, Integer, String, create_engine

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
