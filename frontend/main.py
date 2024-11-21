import os
from http import HTTPMethod

import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from forms import NewCafeForm

API_BASE_URL = os.environ.get('API_BASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

Bootstrap5(app)


@app.get('/')
def list_cafes():
    cafes = requests.get(url=f'{API_BASE_URL}/cafes', params={'sort_by': 'created_on', 'sort_order': 'desc'}).json()
    return render_template(template_name_or_list='index.html', cafes=cafes)


@app.route('/add-cafe', methods=[HTTPMethod.GET, HTTPMethod.POST])
def add_cafe():
    form = NewCafeForm()
    if form.validate_on_submit():
        r = requests.post(url=f'{API_BASE_URL}/cafes', data=form.data)
        r.raise_for_status()
        return redirect(url_for('list_cafes'))
    return render_template(template_name_or_list='add_cafe.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, port=80)
