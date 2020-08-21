import click
from sklearn.preprocessing import RobustScaler

from codigo.desafio_iafront.data.saving import save_partitioned
from codigo.desafio_iafront.jobs.common import prepare_dataframe, transform
from codigo.desafio_iafront.jobs.constants import DEPARTAMENTOS,  GET_DUMMIES_DEPARTAMENTOS 
from codigo.desafio_iafront.jobs.clusters.pca import pca

@click.command()
@click.option('--visitas-com-conversao', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--departamentos', type=str, default="", help="Departamentos separados por virgula")
def main(visitas_com_conversao, saida, data_inicial, data_final, departamentos):
    if len(departamentos) == 0:
        departamentos_lista = DEPARTAMENTOS
    else: 
        departamentos_lista = [departamento.strip() for departamento in departamentos.split(",")]

    result = prepare_dataframe(departamentos_lista, visitas_com_conversao, data_inicial, data_final, get_dummies_departamentos= GET_DUMMIES_DEPARTAMENTOS)
    
    # Faz a escala dos valores
    result_scaled = transform(result, RobustScaler())
    result_scaled = pca(result_scaled)
    # salva resultado
    save_partitioned(result_scaled, saida, ['data', 'hora'])


if __name__ == '__main__':
    main()
