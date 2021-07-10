import pickle
import numpy as np
import pandas as pd


def standardize(array, model_type, days_ahead):
    file_name = f"scaler_XGB_{days_ahead}_{model_type}.pickle"
    with open("./leishmaniasis/model_files/" + file_name,
              "rb") as scalar_pickle:
        scaler_load = pickle.load(scalar_pickle)
    scaled = scaler_load.transform(array)
    return scaled


def model_calculate(scaled_new, model_type, days_ahead):
    file_name = f"model_XGB_{days_ahead}_{model_type}.pickle"
    with open("./leishmaniasis/model_files/" + file_name,
              "rb") as model_pickle:
        model_load = pickle.load(model_pickle)
    xg_pk = model_load.predict(scaled_new)
    return xg_pk


def destandardize(array, model_type, days_ahead):
    file_name = f"scaler_XGB_{days_ahead}_{model_type}.pickle"
    with open("./leishmaniasis/model_files/" + file_name,
              "rb") as scalar_pickle:
        scaler_load = pickle.load(scalar_pickle)
    inverted = scaler_load.inverse_transform(array)
    predict = inverted[:, -1:]
    predict.reshape(1, )
    return predict


def make_prediction(temporal_variables_list, model_type, days_ahead):
    temporal_variables_list.append(
        temporal_variables_list[len(temporal_variables_list) - 1])
    temporal_variables_list = np.array(temporal_variables_list).reshape(1, -1)
    scaled = standardize(temporal_variables_list, model_type, days_ahead)
    scaled_new = np.delete(scaled[0], len(scaled[0]) - 1, 0)
    scaled_new = scaled_new.reshape(1, -1)

    xg_pk = model_calculate(scaled_new, model_type, days_ahead)
    scaled_new_result = np.append(scaled_new, xg_pk[0])
    scaled_new_result = scaled_new_result.reshape(1, -1)

    predict = destandardize(scaled_new_result, model_type, days_ahead)
    return predict[0][0]


def get_varibale_list_from_excel(file, model_type):
    columns_info = {"temporales": ['EVI', 'Precipitación', 'Temperatura', 'Número de casos'],
                    "casos": ['Número de casos'],
                    "todas": ['DIMENSIÓN ECONOMICA', 'DIMENSIÓN CALIDAD DE VIDA',
                              'Número de personas secuestradas', 'Número de personas desplazadas',
                              'Crecimiento_Pob', 'Hectareas_Coca', 'total_poblacion',
                              'DIMENSION URBANA ', 'areakm2', 'antropica', 'bosques',
                              'cultivos.transitorios', 'herbazales', 'mosaico', 'pastos',
                              'vegetacion.secundaria', 'zonas.acuaticas', 'otras.coberturas', 'arido',
                              'seco', 'humedo', 'pluvial', 'msnm', 'minmsnm', 'maxmsnm', 'rango.msnm',
                              'deforestacion05.16', 'cuerpos.de.agua', 'zos.inundables',
                              'zos.susceptibles.de.inundacion', 'max.temperatura', 'min.temperatura',
                              'Cobertura neta en educación secundaria',
                              'Puntaje promedio Pruebas Saber 11 - Lectura crítica',
                              'Cobertura vacunación pentavalente en menores de 1 año',
                              'Densidad poblacional',
                              'Tasa de homicidios (x cada 100.000 habitantes)', 'min.precipitacion',
                              'max.precipitacion',
                              'Tasa de mortalidad infantil en menores de 5 años ',
                              'Cobertura de acueducto (REC)',
                              'Tasa de hurtos (x cada 100.000 habitantes)', 'Disparidades_Económicas',
                              'DIMENSIÓN SEGURIDAD', 'cultivos.permanentes',
                              'Ingresos totales per cápita',
                              'EVI', 'Precipitación', 'Temperatura', 'Número de casos']
                    }

    df = pd.read_excel(file, skiprows=4, index_col=1)
    df = df[columns_info[model_type]]
    temp_var_list = np.flip(df.values, axis=0).flatten('F')
    temp_var_list = temp_var_list[~np.isnan(temp_var_list)]
    return list(temp_var_list)
