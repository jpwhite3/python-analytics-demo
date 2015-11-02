from bokeh.server.utils.plugins import object_page
from bokeh.server.app import bokeh_app
from bokeh.crossfilter.models import CrossFilter
import pandas as pd

# Load our data into a DataFrame
data = pd.read_excel('./output/server_data.xls')

@bokeh_app.route("/bokeh/crossfilter/")
@object_page("crossfilter")
def make_crossfilter():
    data['date'] = data['date'].astype(str)
    app = CrossFilter.create(df=data)
    return app