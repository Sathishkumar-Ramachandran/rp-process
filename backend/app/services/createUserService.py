from flask import Flask
import uuid
#from index import bcrypt
from config.mongoConnection import user_collection, userDetails_Collection
from flask_bcrypt import Bcrypt

from datetime import date

def createUser(userDetails):
    
    Email = userDetails.get('email')
    Password = userDetails.get("password")
    name = userDetails.get( "name" )
    print(Email, Password, name)
    if not Email or not Password:
        return "Email or Password Not Provided",401
    # Checking if the User already
    existing_user = user_collection.find_one({'email': Email})
    if existing_user:
        return "User already exists", 409  # HTTP status code 409 for conflict
    else:
        #Generate a UUID for the user_id
        user_id = str(uuid.uuid4())
        # Hashing the password using Flask-Bcrypt
        #
        # hashed_password = Bcrypt.generate_password_hash(Password).decode('utf-8')
        try:
            hashed_password = Bcrypt().generate_password_hash(Password).decode('utf-8')

            # Creating a new user document
            new_user = {
                'userid': user_id,
                'name': name,
                'email': Email,
                'password': hashed_password
            }
            # Inserting the user document into the MongoDB collection
            user_collection.insert_one(new_user)

            return "User created successfully", 201  # HTTP status code 201 for created
        except Exception as e:
            return f"Error creating user :{e}",500

def add_userInfo(user):
    if not user:
        return f"Not Valid User", 500
    else:
        userID = user.get('userid')
        #LastUpdated = date.today()
        LastUpdated = date.today().isoformat()  
        role = user.get('role')
        bankname = user.get('bankname')
        
        isUserExist = userDetails_Collection.find_one({
            'userid': userID 
        })

        if isUserExist:
            userDetails_Collection.update_one({
                'userid' : userID,
                'role': role,
                'bankname': bankname,
                'lastUpdated':  LastUpdated
            },{'$set': user})
            
            return "User Information Updated Successfully!", 200
        else:
            userDetails_Collection.insert_one({
               'userid' : userID,
                'role': role,
                'bankname': bankname,
                'lastUpdated':  LastUpdated 
            })
            return "User Information Added Succuessfully", 201