import json
import os
import time
from flask import Blueprint, Response, g, jsonify, render_template, request, url_for
import werkzeug.exceptions
from Application.blueprints.todo.froms import TodoForm
from .models import Todo
from Application import db
from dataclasses import dataclass, asdict, replace
import werkzeug
from icecream import ic
from .ui_components import Modal, FormUI,  Toast, render_toast

bp = Blueprint('TODO', __name__, url_prefix='/todos', static_folder='static', template_folder='templates')



create_todo_modal = Modal(element_id='createTodo', header='Create Todo')

@bp.get('/', endpoint='getAll')
def get_all():
    create_form_ui = FormUI(form=TodoForm(), element_id='CreateForm', hx_post=url_for('TODO.createOne'), hx_swap='beforeend', hx_target='#todos', submit_button_text='Submit')

    todos = db.session.query(Todo).all()
    edit_form_ui_arr = [FormUI(
                        form=TodoForm(title=x.title, description=x.description),
                        element_id='editForm'+str(x.id),
                        hx_post=url_for('TODO.putOne', element_id=x.id),
                        hx_target='#todo'+str(x.id),
                        hx_swap='outerHTML',
                        submit_button_text='Edit')
                        for x in todos]
    edit_todo_modal_arr = [Modal(element_id="editModal"+str(x.id), header='Edit Todo') for x in todos]

    return render_template('index.html', create_form_ui=create_form_ui, create_todo_modal=create_todo_modal, ZIP_todos__edit_form_ui_arr__edit_todo_modal_arr=zip(todos, edit_form_ui_arr, edit_todo_modal_arr))


@bp.post('/create-one', endpoint='createOne')
def create_one():
    form = TodoForm()
    create_form_ui = FormUI(form=form, element_id='CreateForm', hx_post=url_for('TODO.createOne'), hx_swap='beforeend', hx_target='#todos', submit_button_text='Submit')

    time.sleep(1.2)
    if form.validate_on_submit():
        todo = Todo(
            title=form.title.data,
            description=form.description.data,
        )

        if (image:=form.image.data) is not None:
            imagename = ''.join(str(time.time()).split('.')) + '.' + image.filename.split('.')[-1]
            image.save(os.path.join(bp.static_folder, 'TodoImages', imagename))
            todo.imagename = imagename

        db.session.add(todo)
        db.session.commit()
        toast = Toast(header='Todo Added Successfully',icon_name='check-circle-fill')
        edit_todo_modal = Modal(element_id="editModal"+str(todo.id), header='Edit Todo')
        edit_form_ui = FormUI(form=TodoForm(title=todo.title, description=todo.description), element_id='editForm'+str(todo.id), hx_post=url_for('TODO.putOne', element_id=todo.id), hx_target='#todo'+str(todo.id), hx_swap='outerHTML', submit_button_text='Edit')
        return (
                render_template('partial/todo.html', todo=todo, edit_todo_modal=edit_todo_modal, edit_form_ui=edit_form_ui)
            +   render_template('oob/form.html', form_ui=replace(create_form_ui, form=TodoForm(formdata=werkzeug.datastructures.MultiDict(mapping=dict()))), oob_id=create_form_ui.element_id)
            +   (res:=render_toast(toast=toast, events={"resetFormsAndCloseModal": dict(form_id=create_form_ui.element_id, modal_id=create_todo_modal.element_id)}))[0], res[1], res[2]
        )
    
    # IF YOU ARE ONLY SENDING OOB SWAPS THEN PLEASE PLEASE PLEASE ADD [HX-RESWAP : NONE] HEADER THIS WAS HARD TO DEBUG
    return render_template('oob/form.html', form_ui=create_form_ui, oob_id=create_form_ui.element_id),  {"HX-Reswap":"none"}

@bp.delete('/delete-one/<int:element_id>', endpoint='deleteOne')
def delete_one(element_id: int):
    time.sleep(1.2)
    todo_to_delete = Todo.query.get(element_id)
    if todo_to_delete is None:
        raise werkzeug.exceptions.BadRequest('Todo does not exist, try to refresh the page.')
    
    if (filename:=todo_to_delete.imagename) is not None:
        os.remove(os.path.join(str(bp.static_folder), 'TodoImages', filename))

    db.session.delete(todo_to_delete)
    db.session.commit()
    toast = Toast(header='Todo Deleted Successfully',icon_name='trash-fill')
    return render_toast(toast)

@bp.post('/put-one/<int:element_id>', endpoint='putOne')
def put_one(element_id: int):
    form = TodoForm()
    time.sleep(1.2)
    todo_to_update = Todo.query.get(element_id)
    if todo_to_update is None:
        raise werkzeug.exceptions.BadRequest('Todo does not exist, try to refresh the page.')


    edit_form_ui = FormUI(form=form, element_id='editForm'+str(todo_to_update.id), hx_post=url_for('TODO.putOne', element_id=todo_to_update.id), hx_target='#todo'+str(todo_to_update.id), hx_swap='outerHTML', submit_button_text='Edit')

    if form.validate_on_submit():
        todo_to_update.title = form.title.data
        todo_to_update.description = form.description.data

        if todo_to_update.imagename is not None:
            os.remove(os.path.join(str(bp.static_folder), 'TodoImages', todo_to_update.imagename))
            todo_to_update.imagename = None

        if (image:=form.image.data) is not None:
            imagename = ''.join(str(time.time()).split('.')) + '.' + image.filename.split('.')[-1]
            image.save(os.path.join(str(bp.static_folder), 'TodoImages', imagename))
            todo_to_update.imagename = imagename

        db.session.add(todo_to_update)
        db.session.commit()
        toast = Toast(icon_name='pencil-fill',header='Todo Updated Successfully')
        edit_todo_modal = Modal(element_id="editModal"+str(todo_to_update.id), header='Edit Todo')
        
        return (
                render_template('partial/todo.html', todo=todo_to_update, edit_todo_modal=edit_todo_modal, edit_form_ui=edit_form_ui)
            +   (res:=render_toast(toast=toast, headers={"HX-Trigger": json.dumps({"resetFormsAndCloseModal": dict(modal_id=edit_todo_modal.element_id)})}))[0], res[1], res[2]
        )
    
    return render_template('oob/form.html', form_ui=edit_form_ui, oob_id=edit_form_ui.element_id), {"HX-Reswap":"none"}
