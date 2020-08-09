import click
from sklearn.preprocessing import MaxAbsScaler

from desafio_iafront.data.saving import save_partitioned
from desafio_iafront.jobs.common import prepare_dataframe, transform


@click.command()
@click.option('--visitas-com-conversao', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--departamentos', type=str, help="Departamentos separados por virgula")
def main(visitas_com_conversao, saida, data_inicial, data_final, departamentos):
    departamentos_lista = [departamento.strip() for departamento in departamentos.split(",")]

    result = prepare_dataframe(departamentos_lista, visitas_com_conversao, data_inicial, data_final)

    # Faz a escala dos valores
    result_scaled = transform(result, MaxAbsScaler())

    # salva resultado
    save_partitioned(result_scaled, saida, ['data', 'hora'])


if __name__ == '__main__':
    main()
