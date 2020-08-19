


#Definindo variáveis globais
DATA_INICIAL="01/06/2020"
DATA_FINAL="15/06/2020"
DATA="01062020-15062020"
DEPARTAMENTOS="moveis_sala,eletronicos,perfumaria,dvds_blu_ray,nan,construcao_ferramentas_seguranca,casa_conforto_2,eletrodomesticos_2,artes_e_artesanato,pc_gamer,moveis_decoracao,musica"
PLOTS="../dataset-desafio-ia-front/plots"
SOURCE="../dataset-desafio-ia-front"
TRANSFORM=robust_scaler
CLUSTER_METHOD=kmeans
N_CLUSTERS=4
PARTICAO=dia
.DEFAULT: help
help:
	@echo "Desafio-IA-front"
	@echo "candidata: Gabriela Lewenfus"
	#################################################################################################################################################################
	@echo "Este desafio tem como objetivo analisar a conversão de visitas em pedidos com base em análises semânticas via clusterização"
	@echo "Cada análise depende a escolha de um método de escalamento TRANSFORM e de um método de clusterização CLUSTER_METHOD que devem ser passados como argumentos"
	@echo "As datas iniciais e finais a serem analisadas também devem ser passadas em DATA_INICIAL e DATA_FINAL"
	#################################################################################################################################################################
	@echo "O pipeline da análise:"
	@echo "		*pedidos"
	@echo "			combinar dataframe de visitas e pedidos (e produtos). Os parâmetros são DATA_INICIAL e DATA_FINAL no formato dd/mm/yyyy"

	@echo "		*scale"
	@echo "			escalar as variáveis preco, frete, prazo, longitude, latitude. Os parâmetros são DATA_INICIAL e DATA_FINAL no formato dd/mm/yyyy, DEPARTAMENTOS e TRANSFORM"
	@echo "			as transformações implementadas são normalize, maxabs_scaler, minmax_scaler, robust_scaler, standard_scaler, power_transformer"
	@echo "			note que DATA_INICIAL e DATA_FINAL são importantes para escalamentos que consideram todos os dados"

	@echo "		*scale-plots"
	@echo "			avaliar o escalamento em scatter_plots 2 a 2 e histogramas. Os parâmetros são DATA_INICIAL e DATA_FINAL no formato dd/mm/yyyy, DEPARTAMENTOS e TRANSFORM"

	@echo "		*cluster"
	@echo "			Métodos de clusterização do sklearn.clusters implementado neste pipeline: kmeans, dbscan ward_agg, ." 
	@echo "			Os parâmetros são DATA_INICIAL e DATA_FINAL no formato dd/mm/yyyy, DEPARTAMENTOS e TRANSFORM, N_CLUSTERS"
	@echo "			observar o resultado da clusterização em scatter_plot (5 features reduzidas a 2 por pca)"

	@echo "		*conversao"
	@echo "			Calcula a conversão por cluster por partição de tempo. Os parâmetros são DATA_INICIAL e DATA_FINAL no formato dd/mm/yyyy, CLUSTER_METHOD e TRANSFORM, e PARTICAO"
	@echo "			PARTICAO pode ser minuto, hora ou dia"

	@echo "		*run"
	@echo "			Roda todo pipeline utilizado para gerar os resultados deste desafio para um método de escalamento definito da variável 'transform' "
	@echo " 		O pipeline não inclui o job {prepara-pedidos} visto que este é comum a todos os métodos de escalamento" 
	@echo " 		o comando ``make run`` computa a transformação de escalamento, e gera histogramas e scatter-plots para primeira e segunda semanas do dataset"
	@echo "			" 

install:
	pip3 install -e .

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyc' -exec rm --force {} +
	

pedidos:
	mkdir -p "${SOURCE}/conversao"
	prepara-pedidos --visitas="${SOURCE}/visitas" --pedidos="${SOURCE}/pedidos" --produtos="${SOURCE}/produtos.csv" --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --saida="${SOURCE}/conversao"

scale:
	@echo "scaling data with ${TRANFORM} using data from ${DATA_INICIAL} to ${DATA_FINAL}"
	
	mkdir -p "${SOURCE}/scale/${TRANSFORM}"
	${TRANSFORM} --visitas-com-conversao="${SOURCE}/conversao" --saida="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --departamentos=${DEPARTAMENTOS}


scale-plots:
	mkdir -p "${PLOTS}/${TRANSFORM}/${DATA}"
	scatter --saida="${PLOTS}/${TRANSFORM}/${DATA}/${TRANSFORM}_preco-frete.html" --dataframe-path="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --x_axis=preco --y_axis=frete --cluster_label=convertido --transform=${TRANSFORM}
	scatter --saida="${PLOTS}/${TRANSFORM}/${DATA}/${TRANSFORM}_preco-prazo.html" --dataframe-path="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --x_axis=preco --y_axis=prazo --cluster_label=convertido --transform=${TRANSFORM}
	scatter --saida="${PLOTS}/${TRANSFORM}/${DATA}/${TRANSFORM}_frete-prazo.html" --dataframe-path="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --x_axis=frete --y_axis=prazo --cluster_label=convertido --transform=${TRANSFORM}
	
	histogram --saida="${PLOTS}/${TRANSFORM}/${DATA}/${TRANSFORM}_hist.html" --dataframe-path="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --transform=${TRANSFORM}


cluster:
	mkdir -p "${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"
	${CLUSTER_METHOD} --dataset="${SOURCE}/scale/${TRANSFORM}" --saida="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --number_of_cluster=${N_CLUSTERS} 
	mkdir -p "${PLOTS}/clusters/${DATA}"
	scatter-cluster --saida="${PLOTS}/clusters/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}.html" --dataframe-path="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --cluster_label=cluster_label --n-amostras=5
	tsne --saida="${PLOTS}/clusters/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}_tsne.html" --dataframe-path="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --cluster_label=cluster_label 


conversao:
	mkdir -p "${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"
	conversao --dataset="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}" --saida="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --particao=${PARTICAO}

	mkdir -p "${PLOTS}/conversao/${DATA}"
	conversao-barplot --saida="${PLOTS}/conversao/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}_barplot.html" --dataframe-path="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL}  --transform=${TRANSFORM}_${CLUSTER_METHOD}

	conversao-lineplot --saida="${PLOTS}/conversao/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}_lineplot.html" --dataframe-path="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}" --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --transform=${TRANSFORM}_${CLUSTER_METHOD}

run:

	make scale TRANSFORM=${transform} 
	mkdir -p "${PLOTS}/${transform}/semana1"
	scatter --saida="${PLOTS}/${transform}/semana1/${transform}_preco-frete.html" --dataframe-path="${SOURCE}/scale/${transform}"  --data-inicial='01/06/2020' --data-final='08/06/2020' --x_axis=preco --y_axis=frete --cluster_label=convertido --transform=${transform}
	scatter --saida="${PLOTS}/${transform}/semana1/${transform}_preco-prazo.html" --dataframe-path="${SOURCE}/scale/${transform}"  --data-inicial='01/06/2020' --data-final='08/06/2020' --x_axis=preco --y_axis=prazo --cluster_label=convertido --transform=${transform}
	scatter --saida="${PLOTS}/${transform}/semana1/${transform}_frete-prazo.html" --dataframe-path="${SOURCE}/scale/${transform}"  --data-inicial='01/06/2020' --data-final='08/06/2020' --x_axis=frete --y_axis=prazo --cluster_label=convertido --transform=${transform}
	
	histogram --saida="${PLOTS}/${transform}/semana1/${transform}_hist.html" --dataframe-path="${SOURCE}/scale/${transform}"  --data-inicial='01/06/2020' --data-final='08/06/2020' --transform=${transform}

	mkdir -p "${PLOTS}/${transform}/semana2"
	scatter --saida="${PLOTS}/${transform}/semana2/${transform}_preco-frete.html" --dataframe-path="${SOURCE}/scale/${transform}"  --data-inicial='08/06/2020' --data-final='15/06/2020' --x_axis=preco --y_axis=frete --cluster_label=convertido --transform=${transform}
	scatter --saida="${PLOTS}/${transform}/semana2/${transform}_preco-prazo.html" --dataframe-path="${SOURCE}/scale/${transform}"  --data-inicial='08/06/2020' --data-final='15/06/2020' --x_axis=preco --y_axis=prazo --cluster_label=convertido --transform=${transform}
	scatter --saida="${PLOTS}/${transform}/semana2/${transform}_frete-prazo.html" --dataframe-path="${SOURCE}/scale/${transform}"  --data-inicial='08/06/2020' --data-final='15/06/2020' --x_axis=frete --y_axis=prazo --cluster_label=convertido --transform=${transform}
	
	histogram --saida="${PLOTS}/${transform}/semana2/${transform}_hist.html" --dataframe-path="${SOURCE}/scale/${transform}"  --data-inicial='08/06/2020' --data-final='15/06/2020' --transform=${transform}


	
	make cluster CLUSTER_METHOD=minibatchkmeans TRANSFORM=${transform} 
	make conversao CLUSTER_METHOD=minibatchkmeans TRANSFORM=${transform} 
	
	make cluster CLUSTER_METHOD=dbscan TRANSFORM=${transform} 


	make cluster CLUSTER_METHOD=wardagg TRANSFORM=${transform} 
	make conversao CLUSTER_METHOD=wardagg TRANSFORM=${transform} 
	
	make cluster CLUSTER_METHOD=birch TRANSFORM=${transform} 
	make conversao  CLUSTER_METHOD=birch TRANSFORM=${transform} 
