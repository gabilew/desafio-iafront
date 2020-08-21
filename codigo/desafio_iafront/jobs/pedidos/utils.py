import pandas as pd
import os


from codigo.desafio_iafront.jobs.pedidos.constants import KEPT_COLUNS, COLUMN_RENAMES
from codigo.desafio_iafront.data.dataframe_utils import read_csv, read_partitioned_json
from codigo.desafio_iafront.data.saving import save_partitioned
from codigo.desafio_iafront.jobs.pedidos.constants import SAVING_PARTITIONS
from codigo.desafio_iafront.jobs.common import convert

def _prepare(pedidos_joined: pd.DataFrame) -> pd.DataFrame:
    # Remove colunas resultantes do merge
    
    result_dataset = drop_merged_columns(pedidos_joined)
    # Remove colunas que não serão usada
    result_dataset = result_dataset[KEPT_COLUNS]
    # Renomeia coluna
    result_dataset = result_dataset.rename(columns=COLUMN_RENAMES)

    return result_dataset


def drop_merged_columns(data_frame: pd.DataFrame) -> pd.DataFrame:
    result_dataset = data_frame.copy(deep=True)
    for column in data_frame.columns:
        if column.endswith("_off"):
            result_dataset = data_frame.drop(column, axis=1)
    return result_dataset


def save_prepared(saida: str, visita_com_produto_e_conversao_df: pd.DataFrame, max_size=None):
    """
    prepara o dataframe de visitas combinado com pedidos e produtos e salva
    Args:
        saida (str): caminho do diretório para salvar os novos dados
        visita_com_produto_e_conversao_df (pd.DataFrame): dataframe com todas as informações de visitas e pedidos combinada
        max_size (int, optional): número  máximo de linhas no dataframe por partição de hora. Se None, não há amostragem. Padrão é None.
    """
    prepared = _prepare(visita_com_produto_e_conversao_df)
    if max_size is not None:
        if prepared.shape[0]> max_size:
            prepared = prepared.sample(n=max_size, random_state=1).reset_index(drop=True)
    save_partitioned(prepared, saida, SAVING_PARTITIONS)


def merge_visita_produto(data_str: str, hour: int, pedidos_df: pd.DataFrame, produtos_df: pd.DataFrame, visitas_df: pd.DataFrame) -> pd.DataFrame:
    """
    Combina os dataframes de visitas, pedidos e produtos

    Args:
        data_str (str): data da visita no format ["%d/%m/%Y"]
        hour (int): hora da visita
        pedidos_df (pd.DataFrame): dataframe referente aos pedidos
        produtos_df (pd.DataFrame): dataframe referente aos produtos 
        visitas_df (pd.DataFrame): dataframe referente às visitas

    Returns:
        pd.DataFrame: dataframe com todas as informações combinadas
    """
    visita_com_produto_df = visitas_df.merge(produtos_df, how="inner", on="product_id", suffixes=("", "_off"))
    visita_com_produto_e_conversao_df = visita_com_produto_df.merge(pedidos_df, how="left", on="visit_id", suffixes=("", "_off"))
            
    visita_com_produto_e_conversao_df["data"] = data_str
    visita_com_produto_e_conversao_df["hora"] = hour
    return visita_com_produto_e_conversao_df



def create_pedidos_df(date_partition: str, hour_snnipet: str, pedidos: str) -> pd.DataFrame:
    """
    Cria dataframe de pedidos

    Args:
        date_partition (str): data do dataframe a ser carregado
        hour_snnipet (str): hora do dataframe a ser carregado
        pedidos (str): caminho para diretório de pedidos 

    Returns:
        pd.DataFrame: dataframe de pedidos
    """
    pedidos_partition = os.path.join(pedidos, date_partition, hour_snnipet)
    pedidos_df = read_partitioned_json(pedidos_partition)
    pedidos_df["product_id"] = pedidos_df["product_id"].astype(str)
    pedidos_df["visit_id"] = pedidos_df["visit_id"].astype(str)
    return pedidos_df

def create_visitas_df(date_partition: str, hour_snnipet: str, visitas: str) -> pd.DataFrame:
   """
    Cria dataframe de visitas

    Args:
        date_partition (str): data do dataframe a ser carregado
        hour_snnipet (str): hora do dataframe a ser carregado
        pedidos (str): caminho para diretório de visitas 

    Returns:
        pd.DataFrame: dataframe de visitas
    """
    
    visitas_partition = os.path.join(visitas, date_partition, hour_snnipet)
    visitas_df = read_partitioned_json(visitas_partition)
    visitas_df["product_id"] = visitas_df["product_id"].astype(str)
    visitas_df["visit_id"] = visitas_df["visit_id"].astype(str)
    return visitas_df