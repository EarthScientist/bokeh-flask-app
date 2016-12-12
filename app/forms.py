from flask_wtf import Form
from wtforms import SelectField
# from wtforms import validators, ValidationError

class DropDown( Form ):
    cols = SelectField( 'Columns' )
    
    def __init__( self, *args, **kwargs ):
        super( DropDown, self ).__init__( *args, **kwargs )
        colnames = [ u'High', u'Low', u'Close', u'Adj. Volume' ]
        self.cols.choices = zip( range( len( colnames ) ), colnames )
