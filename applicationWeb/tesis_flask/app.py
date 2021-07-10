from flask import Flask
from leishmaniasis.leishmaniasis import leishmaniasis_bp
from ophidian_accident.ophidianaccident import ophidianaccident_bp
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={r"/api": {"origins": "*"}})

app.register_blueprint(leishmaniasis_bp, url_prefix="/api/leishmaniasis")
app.register_blueprint(ophidianaccident_bp, url_prefix="/api/ophidianaccident")

if __name__ == "__main__":
    app.run(debug=True)
    