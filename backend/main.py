import http

import flask
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, select
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


# CreateDB
class Base(DeclarativeBase):
    pass


# Connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Table CAFE
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(250))
    coffee_price: Mapped[str] = mapped_column(String(250))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


def str_to_bool(string):
    if string and string.lower() in ['1', 'yes', 'true', 't']:
        return True
    return False


@app.route('/')
def home():
    return render_template('index.html')


@app.get('/cafes')
def cafes_get():
    q_sort_by = request.args.get('sort_by')
    q_sort_order = request.args.get('sort_order')
    query = select(Cafe)

    if q_sort_by in [column.name for column in Cafe.__table__.columns]:
        if q_sort_order == 'desc':
            query = query.order_by(db.desc(getattr(Cafe, q_sort_by)))
        else:
            query = query.order_by(getattr(Cafe, q_sort_by))

    results = db.session.scalars(query).all()
    cafes = [cafe.to_dict() for cafe in results]
    return flask.jsonify(cafes)


@app.get('/cafes/random')
def cafes_get_random():
    random_cafe = db.session.execute(db.select(Cafe).order_by(db.sql.func.random()).limit(1)).scalar()
    return flask.jsonify(cafe=random_cafe.to_dict())


@app.get('/cafes/search-by-location')
def cafes_get_search_by_location():
    q_location = request.args.get('loc')
    cafes = db.session.execute(db.select(Cafe).where(Cafe.location == q_location).order_by(Cafe.name)).scalars()
    if not cafes:
        return flask.jsonify({"message": "Sorry, we don't have any cafe registered at this location."}), 404
    return flask.jsonify([cafe.to_dict() for cafe in cafes])


@app.get('/cafes/<int:cafe_id>')
def cafes_get_by_id(cafe_id: int):
    try:
        cafe = db.get_or_404(Cafe, ident=cafe_id)
        return flask.jsonify(cafe.to_dict()), 200
    except HTTPException as error:
        return flask.jsonify({"message": f"Cafe with id '{cafe_id}' not found"}), error.code


@app.post('/cafes')
def cafes_post():
    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('location'),
        seats=request.form.get('seats'),
        has_toilet=str_to_bool(request.form.get('has_toilet')),
        has_wifi=str_to_bool(request.form.get('has_wifi')),
        has_sockets=str_to_bool(request.form.get('has_sockets')),
        can_take_calls=str_to_bool(request.form.get('can_take_calls')),
        coffee_price=request.form.get('coffee_price')
    )
    db.session.add(new_cafe)
    db.session.commit()
    return flask.jsonify(new_cafe.to_dict()), 201


@app.patch('/cafes/<int:cafe_id>')
def cafes_patch(cafe_id: int):
    try:
        cafe = db.get_or_404(Cafe, ident=cafe_id)
    except HTTPException as error:
        if error.code == 404:
            return flask.jsonify({"message": f"Cafe with id '{cafe_id}' was not found."}), error.code


@app.delete('/cafes/<int:cafe_id>')
def cafes_delete(cafe_id: int):
    q_api_key = request.args.get('api-key')
    if q_api_key != "TopSecretAPIKey":
        return flask.jsonify({"message": "Sorry, that's not allowed. Make sure you're sending the correct api key"}), 403

    try:
        cafe = db.get_or_404(Cafe, ident=cafe_id)
        db.session.delete(cafe)
        db.session.commit()
        return flask.Response(status=http.HTTPStatus.NO_CONTENT)
    except HTTPException as error:
        if error.code == 404:
            return flask.jsonify({"message": f"Cafe with id '{cafe_id}' was not found."}), error.code
        else:
            print(error)
            return flask.jsonify({"message": f"An error occurred while trying to delete the Cafe with ID '{cafe_id}'."}), error.code


if __name__ == '__main__':
    app.run(debug=True)
