import flask
import datetime

# Create a flask instance
app = flask.Flask(__name__)

# When someone goes to the base URL,
# run this function
# (Note: the @ is called a "decorator" in Python: 
# https://www.learnpython.org/en/Decorators)
@app.route('/')
def hello():
    # Just return the following text
    # Note #1: three quotes allows you to provide
    # very long strings
    # Note #2: the <a> tag allows you to make a link
    # Note #3: <br> is the tag for a line break
    return """Hello, World!<br />
Click <a href="time">here</a> for the time"""

# Now support multiple URLs
@app.route('/time')
def time():
    return "Now: {}".format(datetime.datetime.now())

# When this program is run, start flask!
if __name__ == '__main__':
	app.run()
