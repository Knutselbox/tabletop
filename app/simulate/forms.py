from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
import sqlalchemy as sa
from flask_babel import _, lazy_gettext as _l
from app import db
from app.models import User

import datetime
from wtforms.fields import DateField



class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class DateForm(FlaskForm):
    entrydate = DateField(_l('Select date'), format='%Y-%m-%d', render_kw={
                                          'min': datetime.date(2023,1,1).strftime("%Y-%m-%d"),
                                          'max': datetime.date(2023,12,31).strftime("%Y-%m-%d"),
                                          })
    submit = SubmitField(_l('Submit'))
