# # # # NEW FORM TESTING 
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError

class ContactForm( Form ):
    language = SelectField( 'Languages', choices = [('cpp', 'C++'), ('py', 'Python')] )
    submit = SubmitField( "Send" )

# # # # END NEW FORM TESTING 
