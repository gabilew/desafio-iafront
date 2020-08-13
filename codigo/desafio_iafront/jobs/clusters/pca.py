
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np

def pca(dataframe: pd.DataFrame):
    transformer = PCA(n_components=2)
    vector = np.asarray(list(dataframe['features'].to_numpy()))
    new_axis = transformer.fit_transform(vector)
   
    dataframe['new_x_axis'] = new_axis.T[0]
    dataframe['new_y_axis'] = new_axis.T[1]

    return dataframe
