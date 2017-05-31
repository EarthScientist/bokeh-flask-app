from flask import render_template, request
from app import app

def read_data( fn='./data/ALF_TEST.json' ):
    from tinydb import TinyDB
    records = TinyDB( fn ).all()
    return records

def select_metric( records, metric ):
    return [ {'domain':domain,'fire_year':rec['fire_year'], 'replicate':rec[ 'replicate' ], metric:rec[ metric ][ domain ]} for rec in records for domain in rec[ metric ].keys() ]

def select_reps( records, reps ):
    if not isinstance( reps, list ):
        reps = list(reps)
    return [ rec for rec in records if rec['replicate'] in reps ]

def select_years( records, years ):
    if not isinstance( years, list ):
        years = list( years )
    return [ rec for rec in records if rec['fire_year'] in years ]



def make_figure( col ):
    import requests
    from bokeh.plotting import figure, show
    from bokeh.embed import components
    from bokeh.resources import INLINE
    import pandas as pd
    import numpy as np

    # read in the data from the JSON file output from ALF_PP
    reps = [str(i) for i in [1,3,5,7,9]]
    years = [str(i) for i in range( 2001, 2050 )]
    metric = 'total_area_burned'
    domain = 'AOI_SERDP'
    dat = select_metric( select_years( select_reps( read_data(), reps ), years ), metric )
    df = pd.DataFrame( dat )
    df = df[ df.domain == domain ]

    replicates = df.pop( 'replicate' )
    years = df.pop( 'fire_year' )
    _ = df.pop( 'domain' )
    df.index = pd.MultiIndex.from_tuples( zip(replicates, years) )
    df.index = df.index.rename(['replicates', 'years'])
    # df_repcols = df.unstack().T
    df_rep = df[ df.years == '1' ] # select a rep for testing...

        # stock = "AAPL"
        # api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
        # session = requests.Session()
        # session.mount( 'http://', requests.adapters.HTTPAdapter( max_retries=3 ) )
        # raw_data = session.get( api_url )

        # # wrangle
        # dat = raw_data.json()
        # df = pd.DataFrame.from_records( dat['data'], columns=dat['column_names'] )

    # plot
    TOOLS = "pan,wheel_zoom,box_zoom,reset"
    plot = figure( tools=TOOLS,
                   title='Data from Quandle WIKI set',
                   x_axis_label='date',
                   x_axis_type='datetime' )

    if col is None:
        col = 'High'
    
    print( col + 'make' )
    plot.line( pd.to_datetime( df.get( 'Date' ) ), df.get( col ), color='#A6CEE3', legend=stock )
    # plot.line( np.array(df.get( 'Date' )), np.array(df.get( 'High' )), color='#A6CEE3', legend=stock )
    return plot

@app.route('/')
@app.route('/index',  methods=['GET', 'POST'])
def index():
    import requests
    from bokeh.plotting import figure, show
    from bokeh.embed import components
    from bokeh.resources import INLINE
    import pandas as pd
    import numpy as np
    from forms import DropDown
    
    form = DropDown()

    if request.method == 'POST':
        print( 'post' )
        col = form.data[ 'cols' ]
        print( col )
        col_id, col_name = form.cols.choices[ int(col) ]
        print( col_name )

        plot = make_figure( col=col_name )
        header = 'AAPL {}'.format( col_name )

        script, div = components( plot )
        
        return render_template('index.html', script=script, div=div, header=header, form=form )
    elif request.method == 'GET':
        print( 'get' )
        col_name = None # tmp
        plot = make_figure( col=col_name )
        header = 'AAPL {}'.format( col_name )

        script, div = components( plot )
        
        return render_template('index.html', script=script, div=div, header=header, form=form )
    else:
        BaseException( 'error' )

