from fastapi import APIRouter

import all_routes
from model.pydantic_model import Todo
import operations.to_do as db

todo_route = APIRouter()


@todo_route.post("/create")
def new_todo(doc: Todo):

    todo: str = doc.todo
    res = db.create_to_do(todo)
    return res
# get one
@todo_route.get(all_routes.todo_one)
def todo_one(_id: int):

    res = db.get_one(_id)
    return res
# get all

@todo_route.get(all_routes.todo_all)
def todo_all():

    res = db.get_all()
    return res

# get update
@todo_route.patch(all_routes.todo_update)
def todo_update(_id: int, doc:Todo):
    doc = dict(doc)
    title: str = doc['todo']


    res = db.update_todo(_id, title)
    return res

# get delete
@todo_route.delete(all_routes.todo_delete)
def todo_update(_id: int):
    res = db.delete_todo(_id)
    return res
