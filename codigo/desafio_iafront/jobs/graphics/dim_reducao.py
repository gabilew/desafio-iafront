import click
import numpy as np
import pandas as pd
from bokeh.io import output_file, save
from functools import partial


from desafio_iafront.jobs.graphics.utils import plot_clusters
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import (filter_date)
from desafio_iafront.jobs.constants import FEATURES, DEPARTAMENTOS, NMAX_POINTS
from bokeh.plotting import figure, output_file, show
from sklearn.manifold import TSNE

@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True), help='caminho para o dataframe')
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False),help= 'caminho para salvar o arquvio .html')
@click.option('--cluster_label', help='field do dataframe para ser usado como legenda do scatter_plot')
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]), help='menor data dos arquvios carregados')
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]), help='maior data dos arquivos carregados')
def main(dataframe_path: str, saida: str,  cluster_label, data_inicial, data_final):

    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(file_path=dataframe_path, filter_function=filter_function)
    drop_cols = list(set(dataframe.columns)&set(DEPARTAMENTOS))
    dataframe.drop(columns=drop_cols, inplace =True) 

    print("Dataframe carregado")
    #se o dataframe é muito grande, amostrar para o plot
    #a amostragem não foi balanceada
    if dataframe.shape[0]>NMAX_POINTS:
        dataframe = dataframe.sample(n=NMAX_POINTS, random_state=1).reset_index(drop=True)
    
    output_file(saida)
    #calcular as coordenadas utilizando t-distributed stochastic embedding
    X_coords = TSNE(n_components=2, perplexity=80).fit_transform(np.asarray(list(dataframe[FEATURES].to_numpy()))).T
    dataframe['x_axis'] = X_coords[0]
    dataframe['y_axis'] = X_coords[1]
    dataframe['convertido'] = dataframe['convertido'].apply(lambda x: 'convertido' if x ==1 else 'não convertido')
    print("Dimensão reduzida")
    figura = plot_clusters(dataframe, 'x_axis', 'y_axis', cluster_label)
    save(figura)

if __name__ == "__main__":
    main()