import click
from bokeh.io import output_file, save
from functools import partial
import os

from codigo.desafio_iafront.jobs.graphics.utils import hist
from codigo.desafio_iafront.data.dataframe_utils import read_partitioned_json
from codigo.desafio_iafront.jobs.common import filter_date
from bokeh.plotting import figure, output_file
from bokeh.layouts import gridplot

@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--transform', default='')
def main(dataframe_path: str, saida: str,  data_inicial,  data_final, transform):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)
    
    clusters = dataframe['cluster_label'].unique()
    ncounts = [dataframe[dataframe['cluster_label']==cluster].convertido.mean()*100 for cluster in clusters]
    
    output_file(saida)
    p = figure(x_range=clusters, plot_height=400, title=transform)

    p.vbar(x=clusters, top=ncounts, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.yaxis.axis_label = "Taxa de Conversão %"
    p.xaxis.axis_label = "clusters"

     
    save(p)


if __name__ == '__main__':
    main()
