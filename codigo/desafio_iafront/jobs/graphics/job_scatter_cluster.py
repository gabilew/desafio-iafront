import click
from datetime import timedelta
import pandas as pd
from bokeh.io import output_file, save
from functools import partial


from desafio_iafront.jobs.graphics.utils import plot, plot_clusters
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date
from desafio_iafront.jobs.clusters.pca import pca
from desafio_iafront.jobs.contants import DEPARTAMENTOS
from bokeh.plotting import figure, output_file
from collections import Counter

@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--x_axis')
@click.option('--y_axis')
@click.option('--cluster_label')
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--n-amostras', default=10, help='percentual de amostras a ser utilizado no plot. Padrão é 10%')
def main(dataframe_path: str, saida: str, x_axis, y_axis, cluster_label, data_inicial, data_final, n_amostras):

    assert("reverse" not in dataframe_path)

    delta: timedelta = (data_final - data_inicial)
    date_partitions = [data_inicial + timedelta(days=days) for days in range(0,delta.days+7,7)]

    count = 0 
    print(date_partitions)
    for data_i, data_f in zip(date_partitions[:-1], date_partitions[1:]):  
        print("Carregando:",data_i.date(), '-',data_f.date() )
        filter_function = partial(filter_date, data_inicial=data_i, data_final=data_f)
        _dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function) 
        _dataframe = _dataframe.sample(n=int(n_amostras*_dataframe.shape[0]/100),random_state=1).reset_index(drop=True)
       
        if count == 0:
            drop_cols = list(set(_dataframe.columns)&set(DEPARTAMENTOS.split(",")))
            _dataframe.drop(columns=drop_cols, inplace =True) 
            dataframe=_dataframe
            count+=1
        else:
            _dataframe.drop(columns=drop_cols, inplace =True) 
            dataframe = pd.concat((dataframe,_dataframe))
        
    dataframe = pca(dataframe)

    output_file(saida)

    figura = plot_clusters(dataframe, 'new_x_axis','new_y_axis', cluster_label)
    figura.legend.location='top_right'
    save(figura)


if __name__ == '__main__':
    main()
