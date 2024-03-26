from flask import Flask, jsonify
from config.mongoConnection import user_collection
from flask_bcrypt import check_password_hash
#from index import bcrypt

def userLogin(userdata):

    if not userdata:
        print("Userdata not provided")
    else:
        Email = userdata.get('email')
        Password = userdata.get('password')

        if not Email or not Password:
            return "Email or Password is Missing"
        
        user = user_collection.find_one({ 'email': Email})

        if user:
            userPassword= str(user.get('password'))
            
            if check_password_hash(userPassword, Password):
                userId = user.get('userid')
                
                return userId 
            
            else:
                return "Incorrect Password"
        else:
            return "User Not Found"        