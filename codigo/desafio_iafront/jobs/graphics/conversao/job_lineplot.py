import click
import pandas as pd
from bokeh.io import output_file, save
from functools import partial


from codigo.desafio_iafront.jobs.graphics.utils import set_color
from codigo.desafio_iafront.data.dataframe_utils import read_partitioned_json
from codigo.desafio_iafront.jobs.common import filter_date
from bokeh.plotting import figure, output_file,show

@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--transform', default='')
def main(dataframe_path: str, saida: str,  data_inicial, data_final, transform):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)
    dataframe['tempo'] = dataframe.tempo.apply(pd.to_datetime)
    output_file(saida)
    clusters = dataframe.cluster_label.unique()
    colors = [set_color(_) for _ in clusters]
    p = figure(plot_width=1000, plot_height=400, x_axis_type='datetime', title=transform)
    for i,cluster in enumerate(clusters): 
              
        dataframe_cluster = dataframe[dataframe.cluster_label==cluster].groupby('tempo').min()
        dataframe_cluster.sort_index( inplace=True)    
        p.line(dataframe_cluster.index, dataframe_cluster.taxa_conversao, line_width=2, color=colors[i], legend=cluster)

        
    p.xaxis.axis_label = 'tempo'
    p.yaxis.axis_label = 'Taxa de conversão'

    save(p)


if __name__ == '__main__':
    main()
