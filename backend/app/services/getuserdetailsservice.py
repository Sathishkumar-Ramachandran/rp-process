from flask import Flask
from config.mongoConnection import userDetails_Collection

def getUserDetails(userId):
    if userId:
        try:
            user = userDetails_Collection.find_one({
                'userid': userId
            },
            {'_id': 0})
            return user, 201
        except Exception as e:
            return  None, {"Error":"An error occurred while fetching the User details."},500
    else:
        return  None,{"Error":"No user id provided."},400
