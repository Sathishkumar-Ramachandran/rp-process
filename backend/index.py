from flask import Flask

from app.routes.userRoutes import users_routes
from app.routes.rawDataRoutes import rawdata
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.register_blueprint(users_routes)
app.register_blueprint(rawdata)
#bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(debug=True)