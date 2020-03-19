import flask

app = flask.Flask(__name__)

# 

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

# 

import io
import base64

# 

import pandas as pd
import statsmodels.formula.api as stats

##############################################

@app.route('/')
def home():
    # Read the CSV, get a list of all columns except the last
    wine = pd.read_csv("winequality-red.csv")
    wine_columns = wine.columns.values[:-1]

    # Create a form allowing the user to select a column
    # and a legal output format
    return """Wine Analysis<br />
<form action="/analyze">
    Column: <select name="column">{}</select><br />
    Format: <select name="format"><option value="html">html</option><option value="json">json</option></select><br />
    <input type="submit" />
</form>
""".format("".join(['<option value="{}">{}</option>'.format(col, col) for col in wine_columns]))

def analyze_html(column_x, column_y, x, y, y_predicted, r2, m, b):
    # Output the original data as red dots
    plt.plot(x, y, 'ro', label='Actual')

    # And the predicted line in black
    plt.plot(x, y_predicted, 'k', label='Predicted')

    # Axes labels
    plt.xlabel(column_x)
    plt.ylabel(column_y)

    # Equation of the predicted line, with r^2
    plt.title('{} ~ {:.3f}({}) + {:.3f} (R^2={:.3f})'.format(column_y, m, column_x, b, r2))
    plt.legend()

    # Grab the resulting image
    pic_result = io.BytesIO()
    plt.savefig(pic_result, format='png')

    # Clear the plot (in case future requests are made)
    plt.clf()

    # Produce HTML-friendly version of the picture
    html_pic = base64.encodebytes(pic_result.getvalue()).decode('utf-8')

    # Produce the image + a back link
    return """<img src="data:image/png;base64,{}" /><br /><a href="/">back</a>
""".format(html_pic)

@app.route('/analyze')
def analyze():
    # Get parameters sent by the user
    output_format = flask.request.args.get('format', '')
    column = flask.request.args.get('column', '')

    # Read the CSV
    wine = pd.read_csv("winequality-red.csv")

    # If a legal column (aside from the last)
    if column in wine.columns.values[:-1]:
        # Get the name of the last column
        y_column = wine.columns.values[-1]

        # Perform a linear regression
        # (the Q function takes care of column names with spaces)
        regression = stats.ols(formula='Q("{}") ~ Q("{}")'.format(y_column, column), data=wine).fit()
        
        # Grab x/y data points
        x = list(wine[column].values)
        y = list(wine[y_column].values)

        # Extract regression parameters
        m = regression.params['Q("{}")'.format(column)]
        b = regression.params['Intercept']
        r2 = regression.rsquared
        y_predicted = list(regression.fittedvalues)

        # Produce output based upon the requested format
        if output_format == "html":
            return analyze_html(column, y_column, x, y, y_predicted, r2, m, b)
        elif output_format == "json":
            result = {
                'column':column,
                'r_squared':r2,
                'slope':m,
                'intercept':b
            }

            # Converts to proper JSON and tells
            # the browser to expect it
            return flask.jsonify(result)
    
    # If bad parameters, return home
    return home()

if __name__ == '__main__':
	app.run()
