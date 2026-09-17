# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "c9aa894f-e0ed-43a3-9e5f-4b5a67e8e080",
# META       "default_lakehouse_name": "lh_pipelinefabric",
# META       "default_lakehouse_workspace_id": "cb759fec-f1a9-4607-8542-826938050da3",
# META       "known_lakehouses": [
# META         {
# META           "id": "c9aa894f-e0ed-43a3-9e5f-4b5a67e8e080"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

storage_account_name = "stpedrodataeng01"
container_name = "pipefabric"
access_key = "ACESS_KEY"

spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net",
    access_key
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

file_path = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/vendas_dataset.csv"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Mostrando e exibindo a tabela com PySpark

# CELL ********************

pipe_dr = spark.read.csv(
    file_path,
    header=True,
    inferSchema=False
)

display(pipe_dr)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#Vendo o tipo de dado das colunas#
pipe_dr.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Transformando a coluna QUANTIDADE em inteiro #

from pyspark.sql.functions import col
pipe_dr = pipe_dr.withColumn(
    "quantidade",
    col ("quantidade").cast("int")
)

display(pipe_dr.printSchema())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Renomeando as colunas para ficar claro #

pipe_dr = pipe_dr.withColumnRenamed("cliente", "nome_cliente") \
                 .withColumnRenamed("preco", "preco_unitario")

display(pipe_dr.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Remover colunas desnecessárias #

pipe_dr = pipe_dr.drop("coluna_inutil")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Tratando os valores NULOS #

from pyspark.sql.functions import col
pipe_dr = pipe_dr.fillna({
    "nome_cliente": "Desconhecido",
    "quantidade": 0,
    "preco_unitario": 0
})

display(pipe_dr)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

contar = pipe_dr.count()
display(contar)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Removendo valores duplicados #

pipe_dr = pipe_dr.drop_duplicates()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Criando coluna Derivada a partir de outra #
# Criando coluna preco unitario #

pipe_dr = pipe_dr.withColumn("valor_total", col("quantidade") * col("preco_unitario"))

display(pipe_dr)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Salvando no LakeHouse como Tabela #

pipe_dr.write.format("delta") \
       .mode("overwrite") \
       .saveAsTable("vendas_tratadas")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
