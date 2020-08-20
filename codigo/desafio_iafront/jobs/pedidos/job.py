import os
import click
import pandas as pd
from datetime import timedelta


from desafio_iafront.data.dataframe_utils import read_csv
from desafio_iafront.jobs.pedidos.utils import *

@click.command()
@click.option('--pedidos', type=click.Path(exists=True))
@click.option('--visitas', type=click.Path(exists=True))
@click.option('--produtos', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--max-size', type=int, default=500, help="número máximo de amostras por particão de hora")
def main(pedidos, visitas, produtos, saida, data_inicial, data_final,max_size):
    produtos_df = read_csv(produtos)
    produtos_df["product_id"] = produtos_df["product_id"].astype(str)

    delta: timedelta = (data_final - data_inicial)
    date_partitions = [data_inicial.date() + timedelta(days=days) for days in range(delta.days)]

    for data in date_partitions:
        hour_partitions = list(range(0, 24))

        for hour in hour_partitions:
            date_partition = method_name(data, hour, pedidos, produtos_df, saida, visitas, max_size)            
            print(f"Concluído para {date_partition} {hour}h")
            

def method_name(data: str, hour: int, pedidos: str, produtos_df: pd.DataFrame, saida: str, visitas: str, max_size=None) -> str:
    """Método que cria e combina dataframes com visitas, pedidos e produtos e salva em arquivos json paritionados por 
    departamento, dia e hora, respectivamente

    Args:
        data (str): dia 
        hour (int): hora
        pedidos (str): path do dataframe de pedido
        produtos_df (pd.DataFrame): dataframe de produtos
        saida (str): path para salvar o novo dataframe
        visitas (str): path para o dataframe de visitas

    Returns:
        date_partition str
    """
    hour_snnipet = f"hora={hour}"
    data_str = data.strftime('%Y-%m-%d')
    date_partition = f"data={data_str}"
    
    visitas_df = create_visitas_df(date_partition, hour_snnipet, visitas)
    
    pedidos_df = create_pedidos_df(date_partition, hour_snnipet, pedidos)
    
    visita_com_produto_e_conversao_df = merge_visita_produto(data_str, hour, pedidos_df, produtos_df, visitas_df)
    
    save_prepared(saida, visita_com_produto_e_conversao_df, max_size)

    return date_partition
            
    


if __name__ == '__main__':
    main()
