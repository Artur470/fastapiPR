import sys
sys.path.append('./')

from model.sql_model import Todo
from connection import db_session
import os
import decoders.todo as decode
from sqlalchemy.exc import SQLAlchemyError
import logging


logging.basicConfig(level=logging.INFO)

# create
def create_to_do(todo: str) -> dict:
    try:

        req = Todo(todo=todo)


        db_session.add(req)


        db_session.commit()


        return {
            'status': 'ok',
            'message': 'New todo added successfully',
            'id': req._id
        }
    except SQLAlchemyError as e:

        db_session.rollback()
        logging.error(f"SQLAlchemyError: {str(e)}")
        return {
            'status': 'error',
            'message': f"Database error: {str(e)}"
        }
    except Exception as e:

        logging.error(f"Unexpected error: {str(e)}")
        return {
            'status': 'error',
            'message': f"Unexpected error: {str(e)}"
        }

# get all to-do list
def get_all():
    try:
        res = db_session.query(Todo).all()
        docs = decode.decode_todos(res)
        return {
            'status': 'ok',
            'data': docs
        }
    except Exception as e:
        logging.error(f"Error fetching all todos: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

# get one by id
def get_one(_id: int):
    try:
        criteria = {'_id': _id}
        res = db_session.query(Todo).filter_by(**criteria).one_or_none()
        if res is not None:
            record = decode.decode_todo(res)
            return {
                'status': 'ok',
                'data': record
            }
        else:
            return {
                'status': 'error',
                'message': f'Record with id {_id} does not exist'
            }
    except Exception as e:
        logging.error(f"Error fetching todo by id {_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

# update a todo
def update_todo(_id: int, title: str):
    try:
        criteria = {'_id': _id}
        res = db_session.query(Todo).filter_by(**criteria).one_or_none()
        if res is not None:
            res.todo = title
            db_session.commit()
            return {
                'status': 'ok',
                'message': 'Record updated successfully'
            }
        else:
            return {
                'status': 'error',
                'message': f'Record with id {_id} does not exist'
            }
    except Exception as e:
        logging.error(f"Error updating todo with id {_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

# delete a todo
def delete_todo(_id: int):
    try:
        criteria = {'_id': _id}
        res = db_session.query(Todo).filter_by(**criteria).one_or_none()
        if res is not None:
            db_session.delete(res)
            db_session.commit()
            return {
                'status': 'ok',
                'message': 'Record deleted successfully'
            }
        else:
            return {
                'status': 'error',
                'message': f'Record with id {_id} does not exist'
            }
    except Exception as e:
        logging.error(f"Error deleting todo with id {_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }
