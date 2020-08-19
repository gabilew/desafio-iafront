from functools import partial

import click
import numpy as np

from desafio_iafront.data.saving import save_partitioned
from desafio_iafront.jobs.clusters.clusters import birch
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date
from desafio_iafront.jobs.constants import DEPARTAMENTOS

@click.command()
@click.option('--dataframe', type=click.Path(exists=True), help='caminho para os arquivos escalados')
@click.option('--number_of_cluster', type=click.INT, help='número de centroides a serem calculados')
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False), help='caminho para salvar os arquivos clusterizados')
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]), help='mmenor data dos arquivos carregados')
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]), help='maior data dos arquivos carregados')
@click.option('--drop-departamentos', default=True, help='Se True, as colunas de departamentos são eliminadas')
@click.option('--n-samples', type=float, default=1, help='percentual amostras a serem utilizadas para clsuterização')
def main(dataframe: str, number_of_cluster: int, saida: str, data_inicial, data_final, drop_departamentos, n_samples):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)

    dataframe = read_partitioned_json(file_path=dataframe, filter_function=filter_function)
    if drop_departamentos:
        #dropa as colunas de departamento para reduzir o tamanho do dataframe
        #essa informação não será salva para para análises futuras, por exemplo, checar se mesmas categorias pertencem ao mesmo cluster
        drop_cols = list(set(dataframe.columns)&set(DEPARTAMENTOS))
        dataframe.drop(columns=drop_cols, inplace =True) 
    
    #utiliza apenas uma amostra dos dados
    if n_samples < 1:
        dataframe = dataframe.sample(n=int(n_samples*dataframe.shape[0]), weights='datahora', random_state=1).reset_index(drop=True)

    vector = np.asarray(list(dataframe['features'].to_numpy()))
    coordinates, labels = birch(vector, number_of_cluster)

    dataframe['cluster_coordinate'] = None

    dataframe['cluster_label'] = list(labels)

    save_partitioned(dataframe, saida, ['data', 'hora','cluster_label'])
    save_partitioned(dataframe, saida+"_reverse", ['cluster_label','data', 'hora',])


if __name__ == '__main__':
    main()
