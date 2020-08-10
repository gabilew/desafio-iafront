import click
from bokeh.io import output_file, save
from functools import partial


from desafio_iafront.jobs.graphics.utils import plot
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot

@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--x_axis')
@click.option('--y_axis')
@click.option('--cluster_label')
@click.option('--transform')
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def main(dataframe_path: str, saida: str, x_axis, y_axis, cluster_label, data_inicial, data_final, transform):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)
    print(dataframe.shape)
    dataframe = dataframe.sample(n=int(0.1*dataframe.shape[0]), weights='hora', random_state=1).reset_index(drop=True)
    print(dataframe.shape)
    output_file(saida)

    p1 = plot(dataframe, x_axis, y_axis, 'convertido', title="Original")
    p2 = plot(dataframe, x_axis+"_transformed", y_axis+"_transformed", 'convertido', title=transform)
    p1.xaxis.axis_label = x_axis
    p1.yaxis.axis_label = y_axis
    p1.grid.grid_line_color="white"

    p2.xaxis.axis_label = x_axis
    p2.yaxis.axis_label = y_axis
    p2.grid.grid_line_color="white"
    figura = gridplot([p1,p2], ncols=2, plot_width=400, plot_height=400, toolbar_location=None)
    save(figura)


if __name__ == '__main__':
    main()
