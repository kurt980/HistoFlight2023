from flask import Flask, send_from_directory
from flask_cors import CORS

from service.airport import airport_bp
from service.flight import flight_bp
from service.ticket import ticket_bp
from service.comment import comment_bp
from service.airline import airline_bp
from service.auth import auth_bp

app = Flask(__name__, static_url_path='', static_folder='my_vue/build')
CORS(app)

@app.route("/", defaults={'path':''})
def serve(path):
  return send_from_directory(app.static_folder,'index.html')

@app.errorhandler(404)
def not_found(e):
  return send_from_directory(app.static_folder,'index.html')

app.register_blueprint(airport_bp, url_prefix="/api/")
app.register_blueprint(flight_bp, url_prefix="/api/")
app.register_blueprint(ticket_bp, url_prefix="/api/")
app.register_blueprint(comment_bp, url_prefix="/api/")
app.register_blueprint(airline_bp, url_prefix="/api/")
app.register_blueprint(auth_bp, url_prefix="/auth")
