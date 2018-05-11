from flask import Flask, render_template
from urllib import request, parse
import json
import time


base_url = 'https://api.forismatic.com/api/1.0/'
parameters = [('method', 'getQuote'), ('format', 'json'), ('lang', 'en')]
request_url = base_url + '?' + parse.urlencode(parameters)
request_format = request.Request(request_url)
request_format.add_header('User-Agent', 'quotedaily')


# create the application object
app = Flask(__name__)


# use decorators to link the function to a url
@app.route('/')
def home():
    if time.localtime().tm_hour == 15:
        new_quote()
    quote = get_quote()
    return render_template('index.html', quote=quote[0])


def new_quote():
    url = request.urlopen(request_format).read()
    data = json.loads(url)
    with open('quote.json', 'w') as f:
        json.dump(data, f)


def get_quote() -> (str):
    with open('quote.json', 'r') as f:
        qd = json.load(f)
        return(qd['quoteText'], qd['quoteAuthor'])


app.jinja_env.globals.update(get_quote=get_quote)
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
