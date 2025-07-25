#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired

"""
Form wtf form
"""

class searchForm(FlaskForm):
    """Form for searching user information"""
    name = StringField("Enter your name:", validators=[DataRequired()])
    age = IntegerField("Enter your age:", validators=[DataRequired()])
    sex = SelectField(
        "Select your sex:",
        choices=[
            ("female", "Female")
           ],
        validators=[DataRequired()]
    )
    pregnant = SelectField(
        "Are you pregnant?",
        choices=[
            ("yes", "Yes"),
            ("no", "No")
        ],
        validators=[DataRequired()]
    )
    sexually_active = SelectField(
        "Are you sexually active?",
        choices=[
            ("yes", "Yes"),
            ("no", "No")
        ],
        validators=[DataRequired()]
    )
    health_issue = SelectField(
        "Do you smoke?",
        choices=[
            ("yes", "Yes"),
            ("no", "No")
        ],
        validators=[DataRequired()]
    )
