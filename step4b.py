import flask
import datetime

# There is a bug with Flask+PyPlot,
# these next two lines are the fix
import matplotlib
matplotlib.use('Agg')

# Then import PyPlot as usual
import matplotlib.pyplot as plt

# Useful for capturing input/output in
# variables (e.g., picture data)
import io

# Create a flask instance
app = flask.Flask(__name__)

# When someone goes to the base URL,
# run this function
# (Note: the @ is called a "decorator" in Python: 
# https://www.learnpython.org/en/Decorators)
@app.route('/')
def hello():
    # Similar to a dictionary, see if the parameter
    # "name" has been supplied; if so, return it,
    # otherwise return "World"
    name = flask.request.args.get('name', 'World')

    # Just return the following text
    # Note #1: three quotes allows you to provide
    # very long strings
    # Note #2: the <a> tag allows you to make a link
    # Note #3: <br> is the tag for a line break
    return """Hello, {}!<br />
Click <a href="time">here</a> for the time<br />
Click <a href="pretty">here</a> for a pretty picture<br />
<form action="/">
Input your name: <input type="text" name="name" />
<input type="submit" />
</form>""".format(name)

# Now support multiple URLs
@app.route('/time')
def time():
    return "Now: {}".format(datetime.datetime.now())

# What about pictures?
# This is an alternate method
# that has one function dedicated
# to producing/serving the image (pic_data below)
# and another to referring to it (pic here)
@app.route('/pretty')
def pic():
    return '<img src="/image_data" />'

# On-demand produces a picture
@app.route('/image_data')
def pic_data():
    # Variable to capture the rendered picture
    pic_result = io.BytesIO()

    # Make the graph (as usual)
    plt.plot([1,2,3,5], [1,2,1,2], color="k")

    # Save the picture data to a variable
    plt.savefig(pic_result, format='png')

    # "rewind" to the beginning of the image data
    pic_result.seek(0)

    # send the image data to the browser using a file
    # name that lets flask figure out the file type
    return flask.send_file(pic_result, attachment_filename='plot.png')

# When this program is run, start flask!
if __name__ == '__main__':
	app.run()
