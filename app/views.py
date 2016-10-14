from flask import render_template
from app import app


def make_figure():
    import requests
    from bokeh.plotting import figure, show
    from bokeh.embed import components
    from bokeh.resources import INLINE
    import pandas as pd
    import numpy as np

    stock = "AAPL"
    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)

    # wrangle
    dat = raw_data.json()
    df = pd.DataFrame.from_records( dat['data'], columns=dat['column_names'] )

    # plot
    TOOLS = "pan,wheel_zoom,box_zoom,reset"
    plot = figure( tools=TOOLS,
                   title='Data from Quandle WIKI set',
                   x_axis_label='date',
                   x_axis_type='datetime' )

    plot.line(pd.to_datetime(df.get('Date')), df.get('High'), color='#A6CEE3', legend=stock )
    return plot

@app.route('/')
@app.route('/index')
def index():
    import requests
    from bokeh.plotting import figure, show
    from bokeh.embed import components
    from bokeh.resources import INLINE
    import pandas as pd
    import numpy as np

    plot = make_figure()
    header = 'AAPL Highs'

    script, div = components( plot )
    return render_template('index.html', script=script, div=div, header=header )

