from pymongo import MongoClient

# Establish connection to MongoDB Atlas cluster
client = MongoClient(host='mongodb+srv://sathishspacy2001:IZFB8hT47dKHvfOb@cluster-razorpay.dn2bpl7.mongodb.net/?retryWrites=true&w=majority&appName=cluster-razorpay')

# Access the existing database
db = client["Razorpay"]

# Specify the collection where you want to perform the search
user_collection = db["users"]
userDetails_Collection = db['userDetails']
raw_data_collecction = db["rawdata"]
axis_raw_data_collection = db["axis_rawdata"]

# Now you can perform searches within the specified collections
# For example:
# result = user_collection.find_one({"username": "example_user"})
# This will search for a document in the 'users' collection where the username is 'example_user'
# You can use similar find() or aggregate() methods for more complex queries


# from pymongo import MongoClient

# client = MongoClient(host='mongodb+srv://sathishspacy2001:IZFB8hT47dKHvfOb@cluster-razorpay.dn2bpl7.mongodb.net/?retryWrites=true&w=majority&appName=cluster-razorpay')

# db = client["razorpay"]
# user_collection = db["users"]
# userDetails_Collection = db['userDetails']
# raw_data_collecction = db["rawdata"]
# axis_raw_data_collection = db["axis_rawdata"]

