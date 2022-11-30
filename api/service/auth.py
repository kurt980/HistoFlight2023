from flask import Blueprint, request, abort, jsonify, make_response
from service.db import DB
from utils import sha256
import jwt
from datetime import timedelta, datetime
from functools import wraps
from config import AUTH_KEY

auth_bp = Blueprint("auth", __name__)

db = DB()


def check_password_hash(userPW, authPW):
    return sha256(userPW) == sha256(authPW)

def generateToken(user):
    token = jwt.encode({'user_name': user['user_name'], 'exp': datetime.utcnow() + timedelta(minutes=30)}, AUTH_KEY, "HS256")
    return token

def token_required(func):
    @wraps(func)
    def token_wrapper(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, AUTH_KEY, algorithms=["HS256"])
            current_user = db.search(
                "User", {"user_name": data['user_name']})[0]
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'token is expired'})
        except:
            return jsonify({'message': 'token is invalid'})

        return func(current_user, *args, **kwargs)
    return token_wrapper


@auth_bp.route("/login", methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    user = db.search("User", {"user_name": auth.username})[0]
    if check_password_hash(user['password'], auth.password):
        print(str(datetime.now() - timedelta(minutes=30)))
        token = generateToken(user)

        return jsonify({'token': token})

    return make_response('could not verify',  401, {'Authentication': '"login required"'})


@auth_bp.route("/logout", methods=['POST'])
def logout():
    return "Logout"


@auth_bp.route("/signup", methods=['POST'])
def signup_user():
    try:
        body = request.json.copy()
    except:
        body = request.form.copy()

    if 'first_name' not in body.keys():
        body['first_name'] = ""
    if 'first_name' not in body.keys():
        body['last_name'] = ""
    
    colNames = db.getColumnNames("User")
    for colName in colNames:
        if body.get(colName) is None:
            return "Missing " + colName

    user = db.search("User", {'user_name': body['user_name']})
    if user:
        return jsonify({'message': 'user_name already taken'})

    db.insert("User", {
        'user_name': body['user_name'],
        'password': body['password'],
        'email': body['email'],
        'first_name': body['first_name'],
        'last_name': body['last_name'],
    })

    token = generateToken(body)

    return jsonify({'message': 'registered successfully', 'token': token})

@auth_bp.route("/user")
@token_required
def get_user(current_user):
    return current_user