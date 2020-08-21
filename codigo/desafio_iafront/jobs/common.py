import pandas as pd
import numpy as np
from datetime import datetime
from typing import Sequence
from sklearn.base import TransformerMixin

from codigo.desafio_iafront.data.dataframe_utils import read_partitioned_json
from codigo.desafio_iafront.jobs.constants import FEATURES
from sklearn.cluster import MiniBatchKMeans

def prepare_dataframe(departamentos_lista: Sequence[str], dataset_path, data_inicial: datetime,
                      data_final: datetime, get_dummies_departamentos: bool):
    def filter_function(row):
        return filter_departamento(row, departamentos_lista) and filter_date(row, data_inicial, data_final)

    visitas = read_partitioned_json(dataset_path, filter_function)
    visitas_com_coordenadas = _extracting_coordinates(visitas)
    visitas_com_coordenadas  = _coord_distance(visitas_com_coordenadas)
    visitas_com_conversao = convert(visitas_com_coordenadas)
    
    if get_dummies_departamentos:
        departamentos = pd.get_dummies(visitas_com_conversao["departamento"])
        result = visitas_com_conversao.join(departamentos).drop('departamento', axis=1)
    else:
        result = visitas_com_conversao
    return result


def filter_departamento(row, departamentos_lista: Sequence[str]):
    return row["departamento"] in departamentos_lista


def filter_date(row, data_inicial: datetime, data_final: datetime):
    data = datetime.strptime(row["data"], "%Y-%m-%d")
    return data_inicial <= data < data_final


def _coord_distance(dataframe:pd.DataFrame) -> pd.DataFrame:
    vector = np.asarray(list(dataframe[['latitude','longitude']].to_numpy()))
    model = MiniBatchKMeans(n_clusters=5, random_state=0).fit(vector)
    coords=np.min(model.fit_transform(vector),axis=1)
    dataframe['coord_distance'] = coords
    
    return dataframe

def _extracting_coordinates(dataframe: pd.DataFrame) -> pd.DataFrame:
    expanded_cols = pd.DataFrame(dataframe['coordenadas'].values.tolist(), columns=['latitude', 'longitude'])

    return dataframe.join(expanded_cols).drop('coordenadas', axis=1)


def transform(dataframe: pd.DataFrame, scaler: TransformerMixin) -> pd.DataFrame:
    features = FEATURES
    dataframe[features] = dataframe[features].fillna(0)
    fields_to_normalize = dataframe.filter(features).to_numpy()

    feature_scaled = scaler.fit_transform(fields_to_normalize)
    print(len(feature_scaled))
    dataframe['features'] = list(feature_scaled)
    for i,feature in enumerate(features):
        dataframe[feature+"_transformed"] = feature_scaled[:,i] 
    return dataframe


def convert(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe['convertido'] = [_apply_conversion(item) for item in dataframe['id_pedido']]
    return dataframe.drop('id_pedido', axis=1)


def _apply_conversion(product_id):
  
    if product_id is None or not isinstance(product_id,str):
      
        return 0
    else:
        return 1
