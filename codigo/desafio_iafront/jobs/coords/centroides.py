from functools import partial

import click
import numpy as np

from desafio_iafront.data.saving import save_partitioned
from desafio_iafront.jobs.clusters.clusters import minbatchkmeans
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date
from desafio_iafront.jobs.constants import DEPARTAMENTOS


@click.command()
@click.option('--visitas-com-conversao', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--departamentos', deafult=DEPARTAMENTOS, type=str, help="Departamentos separados por virgula")
def main(visitas_com_conversao, saida, data_inicial, data_final, departamentos):

    result = prepare_dataframe(departamentos_lista, visitas_com_conversao, data_inicial, data_final)

    vector = np.asarray(list(dataset[['latitude','longitude']].to_numpy()))
    model = MiniBatchKMeans(n_clusters=5, random_state=0).fit(vector)
    cluster_distance = k.fit_transform(vector)**2
    cluster_label = k.fit(vector)
if __name__ == "__main__":
    main()