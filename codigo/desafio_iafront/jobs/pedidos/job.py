import os
import click
import pandas as pd
from datetime import timedelta


from desafio_iafront.data.dataframe_utils import read_csv
from utils import create_pedidos_df, create_visitas_df, save_prepared, merge_visita_produto

@click.command()
@click.option('--pedidos', type=click.Path(exists=True))
@click.option('--visitas', type=click.Path(exists=True))
@click.option('--produtos', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def main(pedidos, visitas, produtos, saida, data_inicial, data_final):
    produtos_df = read_csv(produtos)
    produtos_df["product_id"] = produtos_df["product_id"].astype(str)

    delta: timedelta = (data_final - data_inicial)
    date_partitions = [data_inicial.date() + timedelta(days=days) for days in range(delta.days)]

    for data in date_partitions:
        hour_partitions = list(range(0, 23))

        for hour in hour_partitions:
            date_partition = method_name(data, hour, pedidos, produtos_df, saida, visitas)            
            print(f"Concluído para {date_partition} {hour}h")
            

def method_name(data: str, hour: int, pedidos: str, produtos_df: pd.DataFrame, saida: str, visitas: str) -> pd.DataFrame:
    """[summary]

    Args:
        data (str): [description]
        hour (int): [description]
        pedidos (str): [description]
        produtos_df (pd.DataFrame): [description]
        saida (str): [description]
        visitas (str): [description]

    Returns:
        pd.DataFrame: [description]
    """
    hour_snnipet = f"hora={hour}"
    data_str = data.strftime('%Y-%m-%d')
    date_partition = f"data={data_str}"
    
    visitas_df = create_visitas_df(date_partition, hour_snnipet, visitas)
    
    pedidos_df = create_pedidos_df(date_partition, hour_snnipet, pedidos)
    
    visita_com_produto_e_conversao_df = merge_visita_produto(data_str, hour, pedidos_df, produtos_df, visitas_df)
    save_prepared(saida, visita_com_produto_e_conversao_df)

    return date_partition
            
    


if __name__ == '__main__':
    main()
