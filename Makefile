


#Definindo variáveis globais
DATA_INICIAL="01/06/2020"
DATA_FINAL="01/07/2020"
DATA="01062020-01072020"
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
	@echo "			Roda todo pipeline utilizado para gerar os resultados deste desafio. Apenas a clusterização kmeans é realizada. " 

install:
	pip install codigo/.

pedidos:
	prepara-pedidos --visitas="${SOURCE}/visitas" --pedidos="${SOURCE}/pedidos" --produtos="${SOURCE}/produtos.csv" --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL}
	

scale:
	@echo "scaling data with ${TRANFORM} using data from ${DATA_INICIAL} to ${DATA_FINAL}"
	
	mkdir -p "${SOURCE}/scale/${TRANSFORM}"
	${TRANSFORM} --visitas-com-conversao="${SOURCE}/conversao" --saida="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --departamentos=${DEPARTAMENTOS}


scale-plots:
	mkdir -p "${PLOTS}/${DATA}"
	scatter --saida="${PLOTS}/${DATA}/${TRANSFORM}_preco-frete.html" --dataframe-path="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --x_axis=preco --y_axis=frete --cluster_label=convertido --transform=${TRANSFORM}
	scatter --saida="${PLOTS}/${DATA}/${TRANSFORM}_preco-prazo.html" --dataframe-path="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --x_axis=preco --y_axis=prazo --cluster_label=convertido --transform=${TRANSFORM}
	scatter --saida="${PLOTS}/${DATA}/${TRANSFORM}_frete-prazo.html" --dataframe-path="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --x_axis=frete --y_axis=prazo --cluster_label=convertido --transform=${TRANSFORM}
	
	histogram --saida="${PLOTS}/${DATA}/${TRANSFORM}_hist2.html" --dataframe-path="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --x_axis=preco,prazo,frete --transform=${TRANSFORM}


cluster:
	mkdir -p "${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"
	${CLUSTER_METHOD} --dataset="${SOURCE}/scale/${TRANSFORM}" --saida="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --number_of_cluster=${N_CLUSTERS} 
	mkdir -p "${PLOTS}/clusters/${DATA}"
	scatter-cluster --saida="${PLOTS}/clusters/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}.html" --dataframe-path="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --cluster_label=cluster_label --n-amostras=5


conversao:
	mkdir -p "${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"
	conversao --dataset="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}" --saida="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --particao=${PARTICAO}

	mkdir -p "${PLOTS}/conversao/${DATA}"
	conversao-barplot --saida="${PLOTS}/conversao/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}_barplot.html" --dataframe-path="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL}  --transform=${TRANSFORM}_${CLUSTER_METHOD}

	conversao-lineplot --saida="${PLOTS}/conversao/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}_lineplot.html" --dataframe-path="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}" --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --transform=${TRANSFORM}_${CLUSTER_METHOD}

run:
	DATA_INICIAL="01/06/2020"
	DATA_FINAL="01/07/2020"
	DATA="01062020-01072020"
	DEPARTAMENTOS="moveis_sala,eletronicos,perfumaria,dvds_blu_ray,nan,construcao_ferramentas_seguranca,casa_conforto_2,eletrodomesticos_2,artes_e_artesanato,pc_gamer,moveis_decoracao,musica"
	PLOTS="../dataset-desafio-ia-front/plots"
	SOURCE="../dataset-desafio-ia-front"

	prepara-pedidos --visitas="${SOURCE}/visitas" --pedidos="${SOURCE}/pedidos" --produtos="${SOURCE}/produtos.csv" --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL}
	#######################################################################################
	TRANSFORM=normalize
	@echo "scaling data with ${TRANFORM} using data from ${DATA_INICIAL} to ${DATA_FINAL}"
	
	mkdir -p "${SOURCE}/scale/${TRANSFORM}"
	${TRANSFORM} --visitas-com-conversao="${SOURCE}/conversao" --saida="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --departamentos=${DEPARTAMENTOS}

	#######################################################################################
	TRANSFORM=robust_scaler
	@echo "scaling data with ${TRANFORM} using data from ${DATA_INICIAL} to ${DATA_FINAL}"
	
	mkdir -p "${SOURCE}/scale/${TRANSFORM}"
	${TRANSFORM} --visitas-com-conversao="${SOURCE}/conversao" --saida="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --departamentos=${DEPARTAMENTOS}

	mkdir -p "${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"
	${CLUSTER_METHOD} --dataset="${SOURCE}/scale/${TRANSFORM}" --saida="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --number_of_cluster=${N_CLUSTERS} 
	mkdir -p "${PLOTS}/clusters/${DATA}"
	scatter-cluster --saida="${PLOTS}/clusters/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}.html" --dataframe-path="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --cluster_label=cluster_label --n-amostras=5

	mkdir -p "${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"
	conversao --dataset="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}" --saida="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --particao=${PARTICAO}

	mkdir -p "${PLOTS}/conversao/${DATA}"
	conversao-barplot --saida="${PLOTS}/conversao/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}_barplot.html" --dataframe-path="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL}  --transform=${TRANSFORM}_${CLUSTER_METHOD}

	conversao-lineplot --saida="${PLOTS}/conversao/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}_lineplot.html" --dataframe-path="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}" --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --transform=${TRANSFORM}_${CLUSTER_METHOD}

	#######################################################################################
	TRANSFORM=standard_scaler
	@echo "scaling data with ${TRANFORM} using data from ${DATA_INICIAL} to ${DATA_FINAL}"
	
	mkdir -p "${SOURCE}/scale/${TRANSFORM}"
	${TRANSFORM} --visitas-com-conversao="${SOURCE}/conversao" --saida="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --departamentos=${DEPARTAMENTOS}

	#######################################################################################
	TRANSFORM=maxabs_scaler
	@echo "scaling data with ${TRANFORM} using data from ${DATA_INICIAL} to ${DATA_FINAL}"
	
	mkdir -p "${SOURCE}/scale/${TRANSFORM}"
	${TRANSFORM} --visitas-com-conversao="${SOURCE}/conversao" --saida="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --departamentos=${DEPARTAMENTOS}

	mkdir -p "${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"
	${CLUSTER_METHOD} --dataset="${SOURCE}/scale/${TRANSFORM}" --saida="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --number_of_cluster=${N_CLUSTERS} 
	mkdir -p "${PLOTS}/clusters/${DATA}"
	scatter-cluster --saida="${PLOTS}/clusters/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}.html" --dataframe-path="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --cluster_label=cluster_label --n-amostras=5

	mkdir -p "${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"
	conversao --dataset="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}" --saida="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --particao=${PARTICAO}

	mkdir -p "${PLOTS}/conversao/${DATA}"
	conversao-barplot --saida="${PLOTS}/conversao/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}_barplot.html" --dataframe-path="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL}  --transform=${TRANSFORM}_${CLUSTER_METHOD}

	conversao-lineplot --saida="${PLOTS}/conversao/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}_lineplot.html" --dataframe-path="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}" --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --transform=${TRANSFORM}_${CLUSTER_METHOD}

	#######################################################################################
	TRANSFORM=minmax_scaler
	@echo "scaling data with ${TRANFORM} using data from ${DATA_INICIAL} to ${DATA_FINAL}"
	
	mkdir -p "${SOURCE}/scale/${TRANSFORM}"
	${TRANSFORM} --visitas-com-conversao="${SOURCE}/conversao" --saida="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --departamentos=${DEPARTAMENTOS}

	#######################################################################################
	TRANSFORM=power_transformer
	@echo "scaling data with ${TRANFORM} using data from ${DATA_INICIAL} to ${DATA_FINAL}"
	
	mkdir -p "${SOURCE}/scale/${TRANSFORM}"
	${TRANSFORM} --visitas-com-conversao="${SOURCE}/conversao" --saida="${SOURCE}/scale/${TRANSFORM}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --departamentos=${DEPARTAMENTOS}

	mkdir -p "${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"
	${CLUSTER_METHOD} --dataset="${SOURCE}/scale/${TRANSFORM}" --saida="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --number_of_cluster=${N_CLUSTERS} 
	mkdir -p "${PLOTS}/clusters/${DATA}"
	scatter-cluster --saida="${PLOTS}/clusters/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}.html" --dataframe-path="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --cluster_label=cluster_label --n-amostras=5

	mkdir -p "${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"
	conversao --dataset="${SOURCE}/cluster/${TRANSFORM}_${CLUSTER_METHOD}" --saida="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --particao=${PARTICAO}

	mkdir -p "${PLOTS}/conversao/${DATA}"
	conversao-barplot --saida="${PLOTS}/conversao/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}_barplot.html" --dataframe-path="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}"  --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL}  --transform=${TRANSFORM}_${CLUSTER_METHOD}

	conversao-lineplot --saida="${PLOTS}/conversao/${DATA}/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}_lineplot.html" --dataframe-path="${SOURCE}/taxa-conversao/${TRANSFORM}_${CLUSTER_METHOD}_conversao_${PARTICAO}" --data-inicial=${DATA_INICIAL} --data-final=${DATA_FINAL} --transform=${TRANSFORM}_${CLUSTER_METHOD}

	