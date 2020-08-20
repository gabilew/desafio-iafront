import os
import click
import pandas as pd
import numpy as np
from datetime import timedelta


from codigo.desafio_iafront.data.dataframe_utils import read_csv
from utils import *
from codigo.desafio_iafront.jobs.constants import DEPARTAMENTOS
from bokeh.plotting import figure, output_file
from bokeh.io import output_file, save

@click.command()
@click.option('--pedidos', type=click.Path(exists=True))
@click.option('--visitas', type=click.Path(exists=True))
@click.option('--produtos', type=click.Path(exists=True))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def main(pedidos, visitas, produtos, data_inicial, data_final):
    produtos_df = read_csv(produtos)
    produtos_df["product_id"] = produtos_df["product_id"].astype(str)

    delta: timedelta = (data_final - data_inicial)
    date_partitions = [data_inicial.date() + timedelta(days=days) for days in range(delta.days)]

    count=0

    conversao_dia={d:[] for d in range(7)}
    conversao_hora={h:[] for h in range(24)}
    count_dia=0
    for data in date_partitions:
        hour_partitions = list(range(0, 24))
    
        for hour in hour_partitions: 
            hour_snnipet = f"hora={hour}"
            data_str = data.strftime('%Y-%m-%d')
            date_partition = f"data={data_str}"  
            print(f"EDA: {date_partition} {hour}h")
            visitas_df = create_visitas_df(date_partition, hour_snnipet, visitas)    
            pedidos_df = create_pedidos_df(date_partition, hour_snnipet, pedidos)    
            visita_com_produto_e_conversao_df = merge_visita_produto(data_str, hour, pedidos_df, produtos_df, visitas_df)

            #checa missing vals
            nan_values = pd.DataFrame(visita_com_produto_e_conversao_df.isna().mean()*100)
            nan=pd.DataFrame()
            nan['cols'] = nan_values.index
            nan['values']=nan_values.values
            nan['index'] = 1
            nan=nan.pivot(index='index',columns='cols')
            try: 

                missing_vals = pd.concat((missing_vals,nan ))
            except: missing_vals = nan
            
            #calcula matriz de correlação com o método de spearman
            visita_com_produto_e_conversao_df["id_pedido"]=visita_com_produto_e_conversao_df.purchase_id
            visita_com_produto_e_conversao_df=convert(visita_com_produto_e_conversao_df)
            df = visita_com_produto_e_conversao_df         
        
            numerical_columns= list(filter(lambda x: "float64"==df[x].dtype or "int64"==df[x].dtype, df.columns))

            df = df[numerical_columns]
            try: 
                corr += df.corr(method='spearman')
            except: corr=df.corr(method='spearman')
            
            #salva summary estatístico do dataframe
           
            if count == 0:
                summary = df.describe()                
            else:
                summary = update_summary(summary, df.describe())
            conversao_dia[count%7].append([df.convertido.sum(),df.shape[0]])
            conversao_hora[count%24].append([df.convertido.sum(),df.shape[0]])
            count+=1
        count_dia+=1
        
    #plota histogram de conversão por dia da semana
    #junta a informação de todas as semanas
    output_file("conversao_dia.html")

    p = figure( plot_height=400, title="Conversão por dia da semana",
           )
    for dia in conversao_dia:
        conversao_dia[dia] = np.array(conversao_dia[dia]).T
    p.vbar(x=list(range(7)), top=[np.sum(conversao_dia[dia][0])/np.sum(conversao_dia[dia][1]) for dia in conversao_dia], width=0.9)
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Taxa de Conversão %"
    p.xaxis.axis_label = "Dias da semana"
    save(p)

    #plota histogram de conversão por hora do dia
    #junta a informação de todos os dias
    output_file("conversao_hora.html")

    p2 = figure( plot_height=400, title="Conversão por hora do dia",
           )
    for hora in conversao_hora:
        conversao_hora[hora] = np.array(conversao_hora[hora]).T
    p2.vbar(x=list(range(24)), top=[np.sum(conversao_hora[hora][0])/np.sum(conversao_hora[hora][1])for hora in conversao_hora], width=0.9)
    p2.xgrid.grid_line_color = None
    p2.yaxis.axis_label = "Taxa de Conversão %"
    p2.xaxis.axis_label = "horas do dia"
    save(p2)


    corr = corr/count
    corr.to_csv("correlation.csv")
    summary.to_csv("summary.csv")
    print(summary)
    missing_vals.to_csv("missing_vals.csv")
         
         

def update_summary(df1, df2):
    """atualiza o dataframe df1 com as informações do df2
    As informações atualizadas são média, desvio padrão, máximo, mínimo e contagem.

    Args:
        df1 (pd.DataFrame): dataframe contendo mean, std, min, max e count
        df2 (pd.Dataframe): dataframe contendo mean, std, min, max e count

    Returns:
        pd.DataFrame: dataframe contendo mean, std, min, max e count acumulado
    """

    df = pd.DataFrame()
    df['count'] = df1.loc['count'] + df2.loc['count']
    
    df['mean'] = (df1.loc['mean']*df1.loc['count'] + df2.loc['mean']*df2.loc['count'])/df['count']
    df['max'] = np.max([df1.loc['max'], df2.loc['max']],axis=0)
    df['min'] = np.min([df1.loc['min'], df2.loc['min']],axis=0)

    df['std'] = np.sqrt((df1.loc['std']**2*df1.loc['count'] + df2.loc['std']**2*df2.loc['count'])/df['count'])
  
    return df.transpose()

if __name__ == '__main__':
    main()
