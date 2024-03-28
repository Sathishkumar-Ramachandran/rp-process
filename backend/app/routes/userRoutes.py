from flask import Blueprint, request, jsonify
from app.services.loginService import userLogin
from app.services.getuserdetailsservice import getUserDetails
from app.services.createUserService import createUser, add_userInfo
from app.services.getallUserService import getUsers
users_routes = Blueprint('users', __name__)

@users_routes.route('/login', methods=['POST'])
def userlogin():
    data = request.get_json()
    if data:
        try:
            userId = userLogin(data)
            return {"userId": userId, "message": "User logged in successfully"}, 201
        except Exception as e:
            print("Error occurred while logging in the user", e)
    else:
        return {"error":"No data received"}

@users_routes.route("/signup", methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)
    if not data:  # Check if data is not empty
        return jsonify({"error": "No data provided"}), 400
    try:
        createUser(data)
        return jsonify({"message":"User created Successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_routes.route('/users/all', methods=['GET'])
def users_all():
    try:
        all_users = getUsers()
        print(all_users)
        return jsonify(all_users)
    except Exception as e:
        return f' Error during fetching users'


@users_routes.route('/userinfo/', methods=['GET'])
def user_profile():
    userid =  request.args.get('userid')
    if userid:
        try:
            user = getUserDetails(userid)
            return jsonify(user)
        except Exception as e:
            return f' Error while fetching user details'
    if user is None:
        return {
            'error': 'Invalid User ID or Error while retrieving UserID'
        }, 404
    else:
        return jsonify(user),  200
        
@users_routes.route('/userinfo', methods=['POST'])
def update_user():
    data = request.get_json()
    try:
        add_userInfo(data)
        return f'User Info Updated Successfully', 201
    except Exception as e:
        return {'error':str(e)}, 500
