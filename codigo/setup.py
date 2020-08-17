from setuptools import setup, find_packages

setup(
    name='desafio_iafront',
    version='',
    packages=find_packages(),
    url='',
    license='',
    author='Time IA-FRONT',
    author_email='',
    description='',
    install_requires=[
        "scikit-learn==0.23.1",
        "click==7.1.2",
        "bokeh==2.1.1",
        "dataset-loader==1.6",
        'pandas==1.1.0',
        'numpy==1.19.1'
    ],
    entry_points={
        'console_scripts': [
            'prepara-pedidos=desafio_iafront.jobs.pedidos:main',
            'normalize=desafio_iafront.jobs.escala_pedidos.job_normalizacao:main',
            'maxabs_scaler=desafio_iafront.jobs.escala_pedidos.job_max_abs_scaler:main',
            'minmax_scaler=desafio_iafront.jobs.escala_pedidos.job_min_max_scaler:main',
            'standard_scaler=desafio_iafront.jobs.escala_pedidos.job_standard_scaler:main',
            'power_transformer=desafio_iafront.jobs.escala_pedidos.job_power_transformer:main',
            'robust_scaler=desafio_iafront.jobs.escala_pedidos.job_robust_scaler:main',
            'scatter=desafio_iafront.jobs.graphics.job_scatter:main',
            'histogram=desafio_iafront.jobs.graphics.job_histogram:main',
            'graphic-clusters=desafio_iafront.jobs.graphics.job_graphics:main',
            'kmeans=desafio_iafront.jobs.clusters.job_kmeans:main',
            'minibatchkmeans=desafio_iafront.jobs.clusters.job_minibatchkmeans:main',
            'dbscan=desafio_iafront.jobs.clusters.job_dbscan:main',
            'wardagg=desafio_iafront.jobs.clusters.job_ward_agg:main',
            'conversao=desafio_iafront.jobs.conversao:main',
            'scatter-cluster=desafio_iafront.jobs.graphics.job_scatter_cluster:main',
            'conversao-lineplot=desafio_iafront.jobs.graphics.conversao.job_lineplot:main',
            'conversao-barplot=desafio_iafront.jobs.graphics.conversao.job_barplot:main'

        ]
    }
)
