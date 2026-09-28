from flask import Flask, jsonify, request, Response
from flask.views import MethodView
from db import Session, User, Advertisement
from sqlalchemy.exc import IntegrityError
from errors import HttpError
from schema import validate, CreateUser, UpdateUser, CreateAdvertisement, UpdateAdvertisement
from flask_bcrypt import Bcrypt

flask_app = Flask("app")
bcrypt = Bcrypt(flask_app)

def hash_password(password: str):
    password = password.encode()
    password = bcrypt.generate_password_hash(password)
    password = password.decode()
    return password

@flask_app.before_request
def before_request():
    session = Session()
    request.session = session

@flask_app.after_request
def after_request(response: Response):
    request.session.close()
    return response

@flask_app.errorhandler(HttpError)
def error_handler(err: HttpError):
    response = jsonify({"error": err.message})
    response.status_code = err.status_code
    return response

def get_user(user_id: int) -> User:
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError("User not found", 404)
    return user

def get_adv(adv_id: int) -> Advertisement:
    adv = request.session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError("Advertisement not found", 404)
    return adv

def add_user(user: User):
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError("User already exists", 400)

def add_adv(adv:Advertisement):
    request.session.add(adv)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError("Advertisement already exists", 400)


class UserView(MethodView):
    def get(self, user_id):
        user = get_user(user_id)
        return jsonify(user.dict)

    def post(self):
        json_data = validate(request.json, CreateUser)
        user = User(name = json_data["name"], 
                    password = hash_password(json_data["password"])
                    )
        add_user(user)
        return jsonify(user.id_dict)

    def patch(self, user_id):
        json_data = validate(request.json, UpdateUser)
        user = get_user(user_id)
        if "name" in json_data:
            user.name = json_data["name"]
        if "password" in json_data:
            user.password = hash_password(json_data["password"])
        add_user(user)
        return jsonify(user.dict)
            
    
    def delete(self, user_id):
        user = get_user(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify ({"message": "deleted"})

class AdvertisementView(MethodView):
    def get(self, adv_id):
        adv = get_adv(adv_id)
        return jsonify(adv.dict)

    def post(self):
        json_data = validate(request.json, CreateAdvertisement)
        get_user(json_data["owner_id"]) 
        adv = Advertisement(title = json_data["title"],
                            description = json_data["description"],
                            owner_id = json_data["owner_id"],
                            )
        add_adv(adv)
        return jsonify(adv.id_dict)
    
    def patch(self, adv_id):
        json_data = validate(request.json, UpdateAdvertisement)
        adv = get_adv(adv_id)
        if "title" in json_data:
            adv.title = json_data["title"]
        if "description" in json_data:
            adv.description = json_data["description"]
        if "owner_id" in json_data:
            get_user(json_data["owner_id"])
            adv.owner_id = json_data["owner_id"]
        add_adv(adv)
        return jsonify(adv.dict)


    def delete(self, adv_id):
        adv = get_adv(adv_id)
        request.session.delete(adv)
        request.session.commit()
        return jsonify({"message": "deleted"})


user_view = UserView.as_view("user")
advertisement_view = AdvertisementView.as_view("advertisement")


flask_app.add_url_rule("/users", view_func=user_view, methods = ["POST"])
flask_app.add_url_rule("/users/<int:user_id>", view_func=user_view, methods = ["GET", "PATCH", "DELETE"])

flask_app.add_url_rule("/advertisements", view_func=advertisement_view, methods = ["POST"])
flask_app.add_url_rule("/advertisements/<int:adv_id>", view_func=advertisement_view, methods = ["GET", "PATCH", "DELETE"])

if __name__ == "__main__":
    flask_app.run()