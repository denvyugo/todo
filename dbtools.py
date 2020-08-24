from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, \
    Column, Date, Integer, String
from datetime import datetime


Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def get_engine():
    """create and return engine of data base"""
    engine = create_engine('sqlite:///todo.db?check_same_tread=False')
    Base.metadata.create_all(engine)
    return engine


def insert_task(engine, task, deadline):
    """add new task to data base"""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    new_task = Task(task=task, deadline=deadline)
    session.add(new_task)
    session.commit()
    session.close()


def get_task(engine, deadline=None):
    """get all tasks for date of deadline"""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    if deadline:
        deadline_ = deadline.date()
        result = session.query(Task).filter_by(deadline=deadline_).all()
    else:
        result = session.query(Task).order_by(Task.deadline).all()
    session.close()
    return result


def get_early_task(engine, date):
    """get all tasks for deadline earlier than date"""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    deadline_ = date.date()
    result = session.query(Task).filter(Task.deadline < deadline_).all()
    session.close()
    return result


def remove_task(engine, task):
    """remove task from data base"""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    session.delete(task)
    session.commit()
    session.close()
