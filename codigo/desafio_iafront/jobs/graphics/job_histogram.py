import click
from bokeh.io import output_file, save
from functools import partial
import os
import numpy as np

from desafio_iafront.jobs.graphics.utils import hist
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date
from desafio_iafront.jobs.constants import FEATURES
from bokeh.plotting import figure, output_file
from bokeh.layouts import gridplot

@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--x_axis',  default=FEATURES)
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--transform', default='')
def main(dataframe_path: str, saida: str, x_axis, data_inicial,  data_final, transform):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)
    convertido = dataframe[dataframe.convertido==1]
    
    if isinstance(x_axis,str):
        x_axis_lista =  x_axis.split(",")
    else:x_axis_lista = x_axis
    saida = os.path.split(saida)
    for x in x_axis_lista:
        filename = os.path.join(saida[0],x+'-'+saida[1])
        output_file(filename)
        print("Criando histograma em "+ filename)
        #original
        x_range = (np.min(dataframe[x]), np.max(dataframe[x])) 
        nunique = dataframe[x].nunique()
   
        if nunique<20:
            bins=nunique
        else: bins=20

        p1 = hist(dataframe, x, x_range, bins=bins, title="Original")
        p3 = hist(convertido, x, x_range, bins=bins, title="Original-Convertido")

        #transformado
        x_range = (np.min(dataframe[x+"_transformed"]), np.max(dataframe[x+"_transformed"]))
        nunique = dataframe[x+"_transformed"].nunique()

        if nunique<20:
            bins=nunique
        else: bins=20
        p2 = hist(dataframe, x+"_transformed",x_range,  bins=bins, title=transform)          
        p4 = hist(convertido, x+"_transformed",x_range, bins=bins, title=transform+"-Convertido")

        figura = gridplot([p1,p2,p3,p4], ncols=2,  plot_width=400, plot_height=400)
        save(figura)


if __name__ == '__main__':
    main()
