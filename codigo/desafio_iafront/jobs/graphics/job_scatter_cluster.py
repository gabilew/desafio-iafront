import click
from bokeh.io import output_file, save
from functools import partial


from desafio_iafront.jobs.graphics.utils import plot, plot_clusters
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date
from desafio_iafront.jobs.clusters.pca import pca
from bokeh.plotting import figure, output_file

@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--x_axis')
@click.option('--y_axis')
@click.option('--cluster_label')
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--n-amostras', default=10, type=int, help='percentual de amostras a ser utilizado no plot. Padrão é 10%')
def main(dataframe_path: str, saida: str, x_axis, y_axis, cluster_label, data_inicial, data_final, n_amostras):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)
    dataframe = dataframe.sample(n=int(n_amostras*dataframe.shape[0]/100), weights='hora', random_state=1).reset_index(drop=True)
    dataframe = pca(dataframe)

    output_file(saida)

    figura = plot_clusters(dataframe, 'new_x_axis','new_y_axis', cluster_label)
    figura.legend.location='top_right'
    save(figura)


if __name__ == '__main__':
    main()
