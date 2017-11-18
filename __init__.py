from flask import Flask, jsonify
import auth
from routes import routes

app = Flask(__name__)

@app.route('/')
def coming_soon():
	return 'Coming soon'

app.register_blueprint(routes)

@app.errorhandler(auth.AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


if __name__ == "__main__":
    app.run()
