import click
from bokeh.io import output_file, save
from functools import partial


from desafio_iafront.jobs.graphics.utils import plot
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot

@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True), help='caminho para o dataframe contendo as colunas de features e labels de cluster')
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False), help='arquivo html para salvar a imagem')
@click.option('--x_axis', help='coluna do dataframe que será aplicada no eixo x')
@click.option('--y_axis', help='coluna do dataframe que será aplicada no eixo y')
@click.option('--cluster_label', help='coluna do dataframe que será aplicada como label')
@click.option('--transform',help='nome da transformação que aparecerá como título no scatter plot transformado')
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]), help='data mínima das visitas que serão utilizadas no plot')
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]), help='data máxima das visitas que serão utilizadas no plot')
@click.option('--n-amostras', default=10, type=int, help='percentual de amostras a ser utilizado no plot. Padrão é 10%')
def main(dataframe_path: str, saida: str, x_axis, y_axis, cluster_label, data_inicial, data_final, transform, n_amostras):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)
    dataframe = dataframe.sample(n=int(n_amostras*dataframe.shape[0]/100), weights='hora', random_state=1).reset_index(drop=True)
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
