from pyspark.sql.types import StructType, StructField, LongType, StringType, FloatType, IntegerType, DateType

SCHEMA = StructType([
    StructField("ANO_BO", LongType(), True),
    StructField("NUM_BO", LongType(), True),
    StructField("NUMERO_BOLETIM", StringType(), True),
    StructField("BO_INICIADO", StringType(), True),
    StructField("BO_EMITIDO", StringType(), True),
    StructField("DATAOCORRENCIA", StringType(), True),
    StructField("HORAOCORRENCIA", StringType(), True),
    StructField("PERIDOOCORRENCIA", StringType(), True),
    StructField("DATACOMUNICACAO", StringType(), True),
    StructField("DATAELABORACAO", StringType(), True),
    StructField("BO_AUTORIA", StringType(), True),
    StructField("FLAGRANTE", StringType(), True),
    StructField("NUMERO_BOLETIM_PRINCIPAL", StringType(), True),
    StructField("LOGRADOURO", StringType(), True),
    StructField("NUMERO", StringType(), True),
    StructField("BAIRRO", StringType(), True),
    StructField("CIDADE", StringType(), True),
    StructField("UF", StringType(), True),
    StructField("LATITUDE", StringType(), True),
    StructField("LONGITUDE", StringType(), True),
    StructField("DESCRICAOLOCAL", StringType(), True),
    StructField("EXAME", StringType(), True),
    StructField("SOLUCAO", StringType(), True),
    StructField("DELEGACIA_NOME", StringType(), True),
    StructField("DELEGACIA_CIRCUNSCRICAO", StringType(), True),
    StructField("ESPECIE", StringType(), True),
    StructField("RUBRICA", StringType(), True),
    StructField("DESDOBRAMENTO", StringType(), True),
    StructField("STATUS", StringType(), True),
    StructField("TIPOPESSOA", StringType(), True),
    StructField("VITIMAFATAL", StringType(), True),
    StructField("NATURALIDADE", StringType(), True),
    StructField("NACIONALIDADE", StringType(), True),
    StructField("SEXO", StringType(), True),
    StructField("DATANASCIMENTO", DateType(), True),
    StructField("IDADE", FloatType(), True),
    StructField("ESTADOCIVIL", StringType(), True),
    StructField("PROFISSAO", StringType(), True),
    StructField("GRAUINSTRUCAO", StringType(), True),
    StructField("CORCUTIS", StringType(), True),
    StructField("NATUREZAVINCULADA", StringType(), True),
    StructField("TIPOVINCULO", StringType(), True),
    StructField("RELACIONAMENTO", StringType(), True),
    StructField("PARENTESCO", FloatType(), True),
    StructField("PLACA_VEICULO", StringType(), True),
    StructField("UF_VEICULO", StringType(), True),
    StructField("CIDADE_VEICULO", StringType(), True),
    StructField("DESCR_COR_VEICULO", StringType(), True),
    StructField("DESCR_MARCA_VEICULO", StringType(), True),
    StructField("ANO_FABRICACAO", FloatType(), True),
    StructField("ANO_MODELO", FloatType(), True),
    StructField("DESCR_TIPO_VEICULO", StringType(), True),
    StructField("QUANT_CELULAR", StringType(), True),
    StructField("MARCA_CELULAR", StringType(), True)
])