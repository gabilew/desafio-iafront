import click
from bokeh.io import output_file, save
from functools import partial

from codigo.desafio_iafront.jobs.constants import  NMAX_POINTS
from codigo.desafio_iafront.jobs.graphics.utils import plot, plot_clusters
from codigo.desafio_iafront.data.dataframe_utils import read_partitioned_json
from codigo.desafio_iafront.jobs.common import filter_date
from codigo.desafio_iafront.jobs.clusters.pca import pca
from bokeh.plotting import figure, output_file

@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--x_axis')
@click.option('--y_axis')
@click.option('--cluster_label')
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def main(dataframe_path: str, saida: str, x_axis, y_axis, cluster_label, data_inicial, data_final):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)
    if dataframe.shape[0]> NMAX_POINTS:
        dataframe = dataframe.sample(n=NMAX_POINTS, weights='hora', random_state=1).reset_index(drop=True)
    dataframe = pca(dataframe)

    output_file(saida)

    figura = plot_clusters(dataframe, 'new_x_axis','new_y_axis', cluster_label)
    figura.legend.location='top_right'
    save(figura)


if __name__ == '__main__':
    main()
