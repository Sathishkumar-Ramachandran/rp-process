from flask import Flask, request, jsonify
from config.mongoConnection import user_collection


def getUsers():
    try:
        users = list(user_collection.find({},{'_id': 0}))
        if users:
            print(users)
            return users
        else:
            return f'Cannot fetch users'
    except Exception as e:
        return f'Error while fetching users: {e}', 500