from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
import pandas as pd
import yaml

app = Flask(__name__)
api = Api(app)

# Load the dataset
with open('winequality.yaml', 'r') as file:
    data = yaml.safe_load(file)
df = pd.DataFrame(data)

class WineQuality(Resource):
    def get(self):
        """Return the entire dataset"""
        data = df.to_dict(orient='records')
        return jsonify(data)

    def post(self):
        """Add a new record to the dataset"""
        new_data = request.json
        df.loc[len(df)] = new_data
        with open('winequality.yaml', 'w') as file:
            yaml.dump(df.to_dict(orient='records'), file)
        return jsonify(new_data)

api.add_resource(WineQuality, '/wine-quality')

# Setup Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Wine Quality API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
