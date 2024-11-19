import os
import requests
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5

API_BASE_URL = os.environ.get('API_BASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

Bootstrap5(app)


@app.get('/')
def list_cafes():
    cafes = requests.get(url=f'{API_BASE_URL}/cafes').json()
    return render_template(template_name_or_list='index.html', cafes=cafes)


if __name__ == "__main__":
    app.run(debug=True, port=80)
