from flask import Flask

from app.routes.userRoutes import users_routes
from app.routes.rawDataRoutes import rawdata
from app.routes.axisDataRoutes import axisData
from app.routes.kotakDataRoutes import kotakData
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.register_blueprint(users_routes)
app.register_blueprint(rawdata)
app.register_blueprint(axisData)
app.register_blueprint(kotakData)
app.secret_key="1245"
#bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(debug=True)