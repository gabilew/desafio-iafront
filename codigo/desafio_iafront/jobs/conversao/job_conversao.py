from functools import partial

import click
import numpy as np
import pandas as pd
from codigo.desafio_iafront.data.saving import save_partitioned
from codigo.desafio_iafront.jobs.clusters.clusters import kmeans
from codigo.desafio_iafront.data.dataframe_utils import read_partitioned_json
from codigo.desafio_iafront.jobs.common import filter_date


@click.command()
@click.option('--dataset', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--particao')
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def main(dataset: str,  saida: str, particao, data_inicial, data_final):

    assert(particao in ['hora','dia','minuto' ])
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)

    dataframe = read_partitioned_json(file_path=dataset, filter_function=filter_function)
    
    
    dataframe['datahora'] = dataframe.datahora.apply(pd.to_datetime)
    if particao == 'minuto':
        dataframe['tempo'] = dataframe.datahora.values.astype('<M8[m]')
    elif particao == 'hora':
        dataframe['tempo'] = dataframe.datahora.values.astype('<M8[h]')
    elif particao == 'dia':
        dataframe['tempo'] = dataframe.datahora.values.astype('<M8[D]')
    


    dataframe['taxa_conversao'] =  dataframe.groupby(['tempo','cluster_label'])['convertido'].transform('mean')
  
    save_partitioned(dataframe, saida, ['cluster_label','tempo' ])


if __name__ == '__main__':
    main()
