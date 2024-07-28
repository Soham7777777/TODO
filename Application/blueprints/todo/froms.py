from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileSize, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

image_extensions = 'jpg jpe jpeg png gif svg bmp webp'.split()

class TodoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=24)], default='', filters=[str.strip], render_kw=dict(placeholder='Todo Title'))
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=2, max=512)], default='', filters=[str.strip], render_kw=dict(placeholder='Todo Description'))
    image = FileField("Add Image", validators=[FileAllowed(image_extensions, "Only images are allowed!"), FileSize(max_size=5000, message="File must be within 5kb size!")])