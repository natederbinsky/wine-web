import flask

# Create a flask instance
app = flask.Flask(__name__)

# When someone goes to the base URL,
# run this function
# (Note: the @ is called a "decorator" in Python: 
# https://www.learnpython.org/en/Decorators)
@app.route('/')
def hello():
    # Just return the following text
    return "Hello, World!"

# When this program is run, start flask!
if __name__ == '__main__':
	app.run()
