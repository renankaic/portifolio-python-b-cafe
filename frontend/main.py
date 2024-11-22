import os
from http import HTTPMethod

import requests
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5, Markup

from forms import NewCafeForm

API_BASE_URL = os.environ.get('API_BASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

Bootstrap5(app)


@app.get('/')
def list_cafes():
    cafes = requests.get(url=f'{API_BASE_URL}/cafes', params={'sort_by': 'created_on', 'sort_order': 'desc'}).json()
    return render_template(template_name_or_list='index.html', cafes=cafes)


@app.route('/cafe-add', methods=[HTTPMethod.GET, HTTPMethod.POST])
def cafe_add():
    form = NewCafeForm()
    if form.validate_on_submit():
        r = requests.post(url=f'{API_BASE_URL}/cafes', data=form.data)
        r.raise_for_status()
        flash(message=Markup('<i class="bi bi-check-circle"></i> The new cafe has been registered successfully!'), category='success')
        return redirect(url_for('list_cafes'))
    return render_template(template_name_or_list='add_cafe.html', form=form)


@app.delete('/cafe-delete/<int:cafe_id>')
def cafe_delete(cafe_id: int):
    r = requests.delete(url=f'{API_BASE_URL}/cafes/{cafe_id}', params={'api-key': 'TopSecretAPIKey'})
    r.raise_for_status()
    if r.ok:
        flash(message=Markup('<i class="bi bi-check-circle"></i> That cafe has been deleted...'),
              category='success')
    else:
        flash(message=Markup('<i class="bi bi-x"</i> An error occurred while trying to delete the cafe!'), category='danger')
    return redirect(url_for('list_cafes')), r.status_code


if __name__ == "__main__":
    app.run(debug=True, port=80)
