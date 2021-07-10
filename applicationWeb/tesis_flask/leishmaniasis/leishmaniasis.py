from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import leishmaniasis.logic as logic
import pandas as pd

leishmaniasis_bp = Blueprint('leishmaniasis_bp', __name__)


@leishmaniasis_bp.route('/predict/from-temporal-variables/<int:days_ahead>',
                        methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def predict_from_temportal_variables(days_ahead):
    variables_list = request.args.get('temporalVariablesList', None)
    variables_list = list(variables_list.split(","))
    prediction = logic.make_prediction(variables_list, "temporales",
                                       days_ahead)
    return jsonify({"Prediction": prediction})


@leishmaniasis_bp.route('/predict/from-cases/<int:days_ahead>',
                        methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def predict_from_cases(days_ahead):
    variables_list = request.args.get('temporalVariablesList', None)
    variables_list = list(variables_list.split(","))
    prediction = logic.make_prediction(variables_list, "casos", days_ahead)
    return jsonify({"Prediction": prediction})


@leishmaniasis_bp.route('/predict/from-all-variables/<int:days_ahead>',
                        methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def predict_from_all_variables(days_ahead):
    variables_list = request.args.get('temporalVariablesList', None)
    variables_list = list(variables_list.split(","))
    prediction = logic.make_prediction(variables_list, "todas", days_ahead)
    return jsonify({"Prediction": prediction})


@leishmaniasis_bp.route('/predict-from-xlsx/<model_type>/<int:days_ahead>', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type'])
def preditc_from_excel(model_type, days_ahead):
    try:
        file = request.files['file']
        variables_list = logic.get_varibale_list_from_excel(file, model_type)
        prediction = logic.make_prediction(
            variables_list, model_type, days_ahead)
        return jsonify({"Prediction": prediction})
    except:
        return "Error, por favor revise la plantilla"
