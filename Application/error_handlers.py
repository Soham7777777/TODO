from dataclasses import asdict
import json
from werkzeug import exceptions
from werkzeug.http import HTTP_STATUS_CODES
from typing import cast
from flask import redirect, url_for

from Application.blueprints.todo.ui_components import Toast, render_toast

def toastify_default_errors(e: exceptions.HTTPException) -> tuple[dict, int]:
    code: int
    description: str | list
    
    if issubclass(type(e), exceptions.InternalServerError):
        UnhandledException = cast(exceptions.InternalServerError, e)
        if UnhandledException.original_exception is not None and any(args:=UnhandledException.original_exception.args):
            description = args[0] if len(args)==1 else list(args)
        else:
            description = UnhandledException.description
        
        code = UnhandledException.code
    else:
        description = e.description # type: ignore
        code = e.code # type: ignore
        toast = Toast(header=HTTP_STATUS_CODES[code],icon_name='patch-exclamation-fill', header_text_color='warning', body=description if type(description) == str else '\n'.join(description))

    return render_toast(toast=toast, status_code=422, headers={"HX-Reswap":"none"})

def handle_notfound_errors(e: exceptions.NotFound):
    return redirect(url_for('home'))