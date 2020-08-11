import click
from bokeh.io import output_file, save
from functools import partial
import os

from desafio_iafront.jobs.graphics.utils import hist
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date
from bokeh.plotting import figure, output_file
from bokeh.layouts import gridplot

@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--x_axis')
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--transform', defaul='')
def main(dataframe_path: str, saida: str, x_axis, data_inicial,  data_final, transform):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)
    dataframe = dataframe.sample(n=int(0.1*dataframe.shape[0]), weights='hora', random_state=1).reset_index(drop=True)
    convertido = dataframe[dataframe.convertido==1]
    
    x_axis_lista =  x_axis.split(",")
    saida = os.path.split(saida)
    for x in x_axis_lista:
        filename = os.path.join(saida[0],x+'-'+saida[1])
        output_file(filename)
        print("Criando histograma em "+ filename)
        p1 = hist(dataframe, x,   title="Original")
        p2 = hist(dataframe, x+"_transformed",  title=transform)    
        p3 = hist(convertido, x,   title="Original-Convertido")
        p4 = hist(convertido, x+"_transformed",  title=transform+"-Convertido")

        figura = gridplot([p1,p2,p3,p4], ncols=2,  plot_width=400, plot_height=400, toolbar_location=None)
        save(figura)


if __name__ == '__main__':
    main()
