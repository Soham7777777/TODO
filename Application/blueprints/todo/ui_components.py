from dataclasses import dataclass
import json
import time
from flask import render_template
from flask_wtf import FlaskForm

@dataclass
class Modal:
    element_id : str
    header: str

@dataclass
class Toast:
    icon_name: str
    header: str
    header_text_color: str = 'primary'
    body: str = ''

def render_toast(toast: Toast, status_code: int=200, events: dict|None=None, headers: dict|None = None):
    element_id = ''.join(str(time.time()).split('.'))
    return render_template('oob/toast.html', toast=toast, element_id=element_id), status_code, {"HX-Trigger-After-Settle": json.dumps({"Toastify":element_id} | (events if events is not None else {}))} | (headers if headers is not None else {})

    # TODO: creating a flashing toast function

@dataclass
class FormUI:
    form: FlaskForm
    element_id: str
    # we can also abstract away htmx elements
    hx_post: str
    hx_swap: str
    hx_target: str
    submit_button_text: str
